#!/usr/bin/env python3
"""
Benchmarking pipeline.

Scans results/ for all generated outputs and evaluates them in parallel:
  - controller entries : test_pass_rate (ground-truth tests) + complexity
  - test entries       : test_pass_rate (ground-truth controller, with coverage)

Each completed evaluation is appended as a JSONL record immediately so that
partial results are preserved even if the run is interrupted.

Usage
-----
    python -m tools.benchmarks.main [options]

    --results-dir DIR      Root results directory  (default: <repo>/results)
    --data-dir    DIR      Ground-truth data dir   (default: <repo>/data)
    --output      FILE     Output .jsonl file      (default: <repo>/pipeline_results.jsonl)
    --workers     N        Parallel workers        (default: cpu_count)
    --mode        {controller,test}                Restrict to one eval type
    --sample      NAME     Restrict to sample(s)  (repeatable)
    --model       NAME     Restrict to model(s)   (repeatable)

JSONL record layout (fields present in every record)
-----------------------------------------------------
    benchmark   : "test_pass_rate" | "complexity"
    sample      : e.g. "AssetPlus"
    tool        : "ecore" | "umple"
    model       : sanitized model name, e.g. "claude_opus_4_7"
    eval_type   : "controller" | "test"
    config      : prompt config, e.g. "feat_gen"
    batch_id    : API batch identifier
    repetition  : "r1", "r2", …
    result_path : absolute path to the evaluated results directory
    timestamp   : ISO-8601 UTC

Additional fields per benchmark
--------------------------------
test_pass_rate  : pass_count, fail_count, error_count, skip_count,
                  total_count, pass_rate, test_cases[], pytest_returncode
                  controller eval only: no coverage (tests run against generated code)
                  test eval only      : coverage{statement_coverage, branch_coverage, …}

complexity      : methods[], aggregate{total_cyclomatic_complexity,
                  avg_cyclomatic_complexity, avg_maintainability_index}
                  (controller eval only)

Error records   : an "error" key replaces the normal result fields.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_RESULTS_DIR = ROOT / "results"
DEFAULT_OUTPUT = ROOT / "pipeline_results.jsonl"


# ── discovery ──────────────────────────────────────────────────────────────────

def discover_entries(results_dir: Path) -> list[dict]:
    """
    Walk results/ and return one metadata dict per valid leaf directory.

    Expected path depth (relative to results_dir):
        {sample}/{tool}/{model}/{eval_type}/{config}/{batch_id}/{rep}
    """
    entries = []
    for path in sorted(results_dir.rglob("*")):
        if not path.is_dir():
            continue
        try:
            parts = path.relative_to(results_dir).parts
        except ValueError:
            continue
        if len(parts) != 7:
            continue
        sample, tool, model, eval_type, config, batch_id, rep = parts
        if eval_type not in ("controller", "test"):
            continue
        if not rep.startswith("r"):
            continue
        if eval_type == "controller" and (path / "controller.py").exists():
            entries.append({
                "sample": sample, "tool": tool, "model": model,
                "eval_type": eval_type, "config": config,
                "batch_id": batch_id, "repetition": rep,
                "result_path": str(path),
            })
        elif eval_type == "test" and any(path.glob("test*.py")):
            entries.append({
                "sample": sample, "tool": tool, "model": model,
                "eval_type": eval_type, "config": config,
                "batch_id": batch_id, "repetition": rep,
                "result_path": str(path),
            })
    return entries


# ── helpers ────────────────────────────────────────────────────────────────────

def _ensure_importable(project_root: str) -> None:
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def _make_record(benchmark: str, entry: dict, timestamp: str, **fields) -> dict:
    """Build an output record with consistent key ordering."""
    return {
        "benchmark": benchmark,
        "sample": entry["sample"],
        "tool": entry["tool"],
        "model": entry["model"],
        "eval_type": entry["eval_type"],
        "config": entry["config"],
        "batch_id": entry["batch_id"],
        "repetition": entry["repetition"],
        "result_path": entry["result_path"],
        "timestamp": timestamp,
        **fields,
    }


def _enrich_tpr(rec: dict, result_path: str) -> dict:
    """
    Re-order a run_benchmark() result dict so metadata comes first, then results.
    Drops the raw controller_path / test_path in favour of result_path.
    """
    META_KEYS = {"sample", "tool", "model", "eval_type", "config", "batch_id", "repetition"}
    rest = {k: v for k, v in rec.items() if k not in META_KEYS | {"timestamp", "controller_path", "test_path"}}
    return {
        "benchmark": "test_pass_rate",
        "sample": rec.get("sample"),
        "tool": rec.get("tool"),
        "model": rec.get("model"),
        "eval_type": rec.get("eval_type"),
        "config": rec.get("config"),
        "batch_id": rec.get("batch_id"),
        "repetition": rec.get("repetition"),
        "result_path": result_path,
        "timestamp": rec.get("timestamp"),
        **rest,
    }


# ── worker functions (module-level so ProcessPoolExecutor can pickle them) ─────

def _run_controller_entry(entry: dict, data_dir: str, project_root: str) -> list[dict]:
    """
    Worker: test_pass_rate + complexity for one generated controller directory.
    """
    _ensure_importable(project_root)
    from tools.benchmarks.testpassrate.benchmark import run_benchmark
    from tools.benchmarks.complexity.helper import iter_python_sources
    from tools.benchmarks.complexity.full_metrics import build_method_reports
    from tools.benchmarks.complexity.code_size import compute_code_size

    result_path = Path(entry["result_path"])
    data_root = Path(data_dir)
    sample, tool = entry["sample"], entry["tool"]
    timestamp = datetime.now(timezone.utc).isoformat()
    records = []

    # ── test pass rate ──────────────────────────────────────────────────────
    try:
        tpr = run_benchmark(
            controller_path=result_path,
            test_path=data_root / sample / "tests",
            data_root=data_root,
            output_file=None,
            sample=sample,
            tool=tool,
            project_root=Path(project_root),
        )
        records.append(_enrich_tpr(tpr, entry["result_path"]))
    except Exception as exc:
        records.append(_make_record("test_pass_rate", entry, timestamp, error=str(exc)))

    # ── complexity ──────────────────────────────────────────────────────────
    try:
        sources = iter_python_sources(result_path)
        methods = []
        for src_path, source in sources:
            for m in build_method_reports(src_path, source):
                methods.append({
                    "method": m["method"],
                    "cyclomatic_complexity": m["cyclomatic_complexity"],
                    "maintainability_index": m["maintainability_index"],
                })
        ccs = [m["cyclomatic_complexity"]["total"] for m in methods]
        mis = [m["maintainability_index"]["score"] for m in methods]
        size = compute_code_size(sources)
        records.append(_make_record(
            "complexity", entry, timestamp,
            methods=methods,
            aggregate={
                "total_cyclomatic_complexity": sum(ccs) if ccs else 0,
                "avg_cyclomatic_complexity": round(sum(ccs) / len(ccs), 4) if ccs else None,
                "avg_maintainability_index": round(sum(mis) / len(mis), 4) if mis else None,
                "total_lines_of_code": size["lines_of_code"],
                "total_characters_of_code": size["characters_of_code"],
            },
        ))
    except Exception as exc:
        records.append(_make_record("complexity", entry, timestamp, error=str(exc)))

    return records


def _run_test_entry(entry: dict, data_dir: str, project_root: str) -> list[dict]:
    """
    Worker: test_pass_rate for one generated test directory against the ground-truth controller.
    Coverage is collected automatically by run_benchmark.
    """
    _ensure_importable(project_root)
    from tools.benchmarks.testpassrate.benchmark import run_benchmark

    result_path = Path(entry["result_path"])
    data_root = Path(data_dir)
    sample, tool = entry["sample"], entry["tool"]
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        tpr = run_benchmark(
            controller_path=data_root / sample / tool / "controller",
            test_path=result_path,
            data_root=data_root,
            output_file=None,
            sample=sample,
            tool=tool,
            project_root=Path(project_root),
        )
        return [_enrich_tpr(tpr, entry["result_path"])]
    except Exception as exc:
        return [_make_record("test_pass_rate", entry, timestamp, error=str(exc))]


# ── main pipeline ──────────────────────────────────────────────────────────────

def run_pipeline(
    results_dir: Path,
    data_dir: Path,
    output_file: Path,
    *,
    workers: int,
    filter_mode: str | None = None,
    filter_samples: list[str] | None = None,
    filter_models: list[str] | None = None,
    project_root: Path = ROOT,
) -> None:
    entries = discover_entries(results_dir)

    if filter_mode:
        entries = [e for e in entries if e["eval_type"] == filter_mode]
    if filter_samples:
        entries = [e for e in entries if e["sample"] in filter_samples]
    if filter_models:
        entries = [e for e in entries if e["model"] in filter_models]

    if not entries:
        print("No matching entries found.")
        return

    total = len(entries)
    print(f"Found {total} result director{'y' if total == 1 else 'ies'} to evaluate.")
    print(f"Output: {output_file}\n")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    root_str = str(project_root)
    data_str = str(data_dir)

    # Counts of result dirs processed per (model, eval_type)
    counts: dict[tuple[str, str], int] = defaultdict(int)
    done = 0

    futures: dict = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for entry in entries:
            fn = _run_controller_entry if entry["eval_type"] == "controller" else _run_test_entry
            futures[pool.submit(fn, entry, data_str, root_str)] = entry

        with open(output_file, "a", encoding="utf-8") as out:
            for fut in as_completed(futures):
                entry = futures[fut]
                key = (entry["model"], entry["eval_type"])
                try:
                    records = fut.result()
                except Exception as exc:
                    timestamp = datetime.now(timezone.utc).isoformat()
                    records = [_make_record("pipeline_error", entry, timestamp, error=str(exc))]

                for rec in records:
                    out.write(json.dumps(rec, ensure_ascii=False))
                    out.write("\n")
                out.flush()

                counts[key] += 1
                done += 1
                print(f"  [{done}/{total}] {entry['model']} / {entry['tool']} / {entry['eval_type']} / "
                      f"{entry['sample']} / {entry['config']} / {entry['repetition']}")

    # ── console summary ────────────────────────────────────────────────────────
    col = max((len(m) for m, _ in counts), default=10)
    print(f"\n{'Model':<{col}}  {'Mode':<12}  {'Entries':>7}")
    print("-" * (col + 24))
    for (model, mode), count in sorted(counts.items()):
        print(f"{model:<{col}}  {mode:<12}  {count:>7}")
    print(f"\nSaved {sum(counts.values())} entries → {output_file}")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate all generated outputs under results/ and write metrics to JSONL.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--results-dir", type=Path, default=DEFAULT_RESULTS_DIR, metavar="DIR",
        help=f"Root results directory (default: {DEFAULT_RESULTS_DIR})",
    )
    parser.add_argument(
        "--data-dir", type=Path, default=DEFAULT_DATA_DIR, metavar="DIR",
        help=f"Ground-truth data directory (default: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT, metavar="FILE.jsonl",
        help=f"Output JSONL file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--workers", type=int, default=max(1, os.cpu_count() or 4), metavar="N",
        help="Number of parallel worker processes (default: cpu_count)",
    )
    parser.add_argument(
        "--mode", choices=["controller", "test"], default=None,
        help="Restrict evaluation to one eval type (default: both)",
    )
    parser.add_argument(
        "--sample", action="append", dest="samples", metavar="NAME",
        help="Restrict to a specific sample (repeatable)",
    )
    parser.add_argument(
        "--model", action="append", dest="models", metavar="NAME",
        help="Restrict to a specific model name (repeatable)",
    )
    args = parser.parse_args(argv)

    run_pipeline(
        results_dir=args.results_dir,
        data_dir=args.data_dir,
        output_file=args.output,
        workers=args.workers,
        filter_mode=args.mode,
        filter_samples=args.samples,
        filter_models=args.models,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
