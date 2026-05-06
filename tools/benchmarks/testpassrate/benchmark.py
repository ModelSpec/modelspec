#!/usr/bin/env python3
"""
Test pass-rate and coverage benchmark.

Sets up a temporary Python package that mirrors the data/ layout, places the
controller and test files in the right positions so that all relative imports
resolve, then invokes pytest with JUnit XML and JSON coverage reports.

Supports two evaluation directions:
  - Controller eval : ground-truth test suite  vs  generated controller.py
  - Test eval       : generated test suite      vs  ground-truth controller.py

Usage
-----
    python -m tools.benchmarks.testpassrate.benchmark \
        --controller <folder containing controller.py> \
        --tests      <folder containing test files>   \
        [--output    results.jsonl]                   \
        [--data-root path/to/data/]                   \
        [--sample    AssetPlus]                       \
        [--tool      ecore|umple]

Path conventions
----------------
Generated artefacts live at:
    results/{sample}/{tool}/{model}/{eval_type}/{config}/{batch_id}/{rep}/

Ground-truth artefacts live at:
    data/{sample}/tests/                   (tests)
    data/{sample}/{tool}/controller/       (controller)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = _THIS_FILE.parents[3]
DEFAULT_DATA_ROOT = PROJECT_ROOT / "data"


# ── metadata extraction ────────────────────────────────────────────────────────

def parse_path_metadata(path: Path, project_root: Path = PROJECT_ROOT) -> dict:
    """Extract sample/tool/model/… from a results/ or data/ path."""
    path = path.resolve()
    results_root = project_root / "results"
    data_root = project_root / "data"

    try:
        parts = path.relative_to(results_root).parts
        # results/{sample}/{tool}/{model}/{eval_type}/{config}/{batch_id}/{rep}/
        keys = ("sample", "tool", "model", "eval_type", "config", "batch_id", "repetition")
        return {"source": "results", **dict(zip(keys, parts))}
    except ValueError:
        pass

    try:
        parts = path.relative_to(data_root).parts
        tool = parts[1] if len(parts) > 1 and parts[1] in ("ecore", "umple") else None
        return {
            "source": "data",
            "sample": parts[0] if parts else None,
            "tool": tool,
        }
    except ValueError:
        pass

    return {}


# ── temp environment setup ─────────────────────────────────────────────────────

def setup_test_environment(
    controller_path: Path,
    test_path: Path,
    sample: str,
    tool: str,
    tmp_dir: Path,
    data_root: Path,
) -> tuple[Path, Path]:
    """
    Build this layout inside tmp_dir:

        tmp_dir/
        ├── conftest.py                   ← copied from data_root (provides mw /
        │                                    --modeling-tool option for ground-truth tests)
        └── {sample}/
            ├── __init__.py
            ├── tests/
            │   ├── __init__.py
            │   └── <test files>          ← from test_path (unchanged content)
            └── {tool}/
                ├── __init__.py
                ├── controller/
                │   ├── __init__.py
                │   └── controller.py     ← from controller_path (unchanged content)
                └── generated_model_layer/
                    └── <model files>     ← from data_root (ground-truth model layer)

    Placing tmp_dir in PYTHONPATH lets Python resolve:
      - "from ..{tool}.controller.controller import …"   (in test files)
      - "from ..generated_model_layer import …"          (in controller)

    Returns (tests_dir, controller_dir).
    """
    sample_dir = tmp_dir / sample
    tool_dir = sample_dir / tool
    controller_dir = tool_dir / "controller"
    tests_dir = sample_dir / "tests"

    for d in (sample_dir, tool_dir, controller_dir, tests_dir):
        d.mkdir(parents=True, exist_ok=True)
        init = d / "__init__.py"
        if not init.exists():
            init.touch()

    # ── controller ──
    ctrl_src = controller_path / "controller.py"
    if not ctrl_src.exists():
        raise FileNotFoundError(f"controller.py not found in {controller_path}")
    shutil.copy2(ctrl_src, controller_dir / "controller.py")

    data_ctrl_init = data_root / sample / tool / "controller" / "__init__.py"
    if data_ctrl_init.exists():
        shutil.copy2(data_ctrl_init, controller_dir / "__init__.py")

    # ── model layer (always from data, unchanged) ──
    model_src = data_root / sample / tool / "generated_model_layer"
    if not model_src.exists():
        raise FileNotFoundError(
            f"generated_model_layer not found at {model_src}"
        )
    shutil.copytree(model_src, tool_dir / "generated_model_layer")

    # ── tests (unchanged content, adjusted location) ──
    for f in sorted(test_path.iterdir()):
        if f.is_file() and f.name != "__init__.py":
            shutil.copy2(f, tests_dir / f.name)
    # Ensure package init even when not present in source
    (tests_dir / "__init__.py").touch()

    # ── root conftest (registers --modeling-tool option and mw fixture) ──
    data_conftest = data_root / "conftest.py"
    if data_conftest.exists():
        shutil.copy2(data_conftest, tmp_dir / "conftest.py")

    # ── pytest.ini — sets rootdir and broadens collection patterns ──
    # Ground-truth files follow camelCase naming (testAddAsset.py, testAddAssetSuccess)
    # rather than pytest's default snake_case patterns (test_*.py, test_*).
    # Generated tests use snake_case, so both patterns must be active.
    (tmp_dir / "pytest.ini").write_text(
        "[pytest]\n"
        "python_files = test*.py\n"
        "python_functions = test*\n",
        encoding="utf-8",
    )

    return tests_dir, controller_dir


# ── pytest invocation ──────────────────────────────────────────────────────────

PYTEST_TIMEOUT_S = 30


def run_pytest(
    tests_dir: Path,
    controller_dir: Path,
    tmp_dir: Path,
    tool: str,
    project_root: Path = PROJECT_ROOT,
) -> dict:
    """
    Run pytest on tests_dir with JUnit XML output and (optionally) coverage.

    PYTHONPATH is extended with:
      - tmp_dir       so "{sample}" is importable as a top-level package
      - project_root  so "tools" (used by data/conftest.py) is importable

    Returns dict with keys: returncode, stdout, stderr, junit_xml, cov_json.
    """
    junit_xml = tmp_dir / "junit.xml"
    cov_json = tmp_dir / "coverage.json"

    cmd = [
        sys.executable, "-m", "pytest",
        str(tests_dir),
        f"--junitxml={junit_xml}",
        f"--modeling-tool={tool}",
        "--tb=short",
        "-q",
        "--no-header",
        f"--cov={controller_dir}",
        "--cov-branch",
        f"--cov-report=json:{cov_json}",
        "--cov-report=term-missing:skip-covered",
    ]

    existing = os.environ.get("PYTHONPATH", "")
    pythonpath = os.pathsep.join(
        p for p in [str(tmp_dir), str(project_root), existing] if p
    )
    env = {**os.environ, "PYTHONPATH": pythonpath}

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(tmp_dir),
            env=env,
            timeout=PYTEST_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"pytest timed out after {PYTEST_TIMEOUT_S} s") from None

    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "junit_xml": junit_xml if junit_xml.exists() else None,
        "cov_json": cov_json if cov_json.exists() else None,
    }


# ── result parsers ─────────────────────────────────────────────────────────────

def parse_junit_xml(xml_path: Path) -> dict:
    """Parse a JUnit XML file into a structured results dict."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    test_cases: list[dict] = []
    pass_count = fail_count = error_count = skip_count = 0

    for tc in root.iter("testcase"):
        classname = tc.get("classname", "")
        name = tc.get("name", "")
        full_name = f"{classname}::{name}" if classname else name
        duration = float(tc.get("time") or 0)

        failure = tc.find("failure")
        error = tc.find("error")
        skipped = tc.find("skipped")

        if failure is not None:
            result, fail_count = "failed", fail_count + 1
            message = (failure.get("message") or failure.text or "")[:400].strip()
        elif error is not None:
            result, error_count = "error", error_count + 1
            message = (error.get("message") or error.text or "")[:400].strip()
        elif skipped is not None:
            result, skip_count = "skipped", skip_count + 1
            message = skipped.get("message", "")
        else:
            result, pass_count = "passed", pass_count + 1
            message = ""

        entry: dict = {
            "name": full_name,
            "result": result,
            "duration_s": round(duration, 4),
        }
        if message:
            entry["message"] = message
        test_cases.append(entry)

    total = pass_count + fail_count + error_count
    return {
        "pass_count": pass_count,
        "fail_count": fail_count,
        "error_count": error_count,
        "skip_count": skip_count,
        "total_count": total,
        "pass_rate": round(pass_count / total, 4) if total > 0 else 0.0,
        "test_cases": test_cases,
    }


def parse_coverage_json(cov_json_path: Path) -> Optional[dict]:
    """
    Parse pytest-cov's JSON coverage report.

    Returns a dict with statement_coverage and (if branch data present)
    branch_coverage, each as a ratio in [0, 1].
    """
    try:
        with open(cov_json_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None

    totals = data.get("totals", {})
    if not totals:
        return None

    out: dict = {
        "statement_coverage": round(totals.get("percent_covered", 0) / 100, 4),
        "covered_lines": totals.get("covered_lines"),
        "num_statements": totals.get("num_statements"),
    }

    num_branches = totals.get("num_branches")
    if num_branches:
        out["branch_coverage"] = round(
            totals.get("covered_branches", 0) / num_branches, 4
        )
        out["covered_branches"] = totals.get("covered_branches")
        out["num_branches"] = num_branches

    return out


# ── public API ─────────────────────────────────────────────────────────────────

def run_benchmark(
    controller_path: Path,
    test_path: Path,
    *,
    data_root: Path = DEFAULT_DATA_ROOT,
    output_file: Optional[Path] = None,
    sample: Optional[str] = None,
    tool: Optional[str] = None,
    project_root: Path = PROJECT_ROOT,
) -> dict:
    """
    Run the test pass-rate and coverage benchmark for one (controller, test) pair.

    Infers sample and tool from the path structure when not supplied explicitly.
    If output_file is given, appends the result as a JSONL line.
    Always returns the result dict (suitable for use with multiprocessing.Pool).

    The returned dict contains:
      timestamp, controller_path, test_path, sample, tool, model, eval_type,
      config, batch_id, repetition,
      pass_count, fail_count, error_count, skip_count, total_count, pass_rate,
      test_cases  (list of per-test dicts),
      coverage    (dict with statement_coverage, branch_coverage, …),
      pytest_returncode.
    """
    controller_path = Path(controller_path).resolve()
    test_path = Path(test_path).resolve()

    ctrl_meta = parse_path_metadata(controller_path, project_root)
    test_meta = parse_path_metadata(test_path, project_root)

    # results/ path carries the richest metadata; prefer it as primary
    if ctrl_meta.get("source") == "results":
        merged = {**test_meta, **ctrl_meta}
    else:
        merged = {**ctrl_meta, **test_meta}

    effective_sample = sample or merged.get("sample")
    effective_tool = tool or merged.get("tool")

    if not effective_sample:
        raise ValueError(
            "Cannot infer sample name from paths. Pass --sample explicitly."
        )
    if not effective_tool:
        raise ValueError(
            "Cannot infer modeling tool from paths. Pass --tool explicitly."
        )

    record: dict = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "controller_path": str(controller_path),
        "test_path": str(test_path),
        "sample": effective_sample,
        "tool": effective_tool,
        "model": merged.get("model"),
        "eval_type": merged.get("eval_type"),
        "config": merged.get("config"),
        "batch_id": merged.get("batch_id"),
        "repetition": merged.get("repetition"),
    }

    with tempfile.TemporaryDirectory(prefix="modelspec_tpr_") as tmp_str:
        tmp_dir = Path(tmp_str)

        tests_dir, controller_dir = setup_test_environment(
            controller_path, test_path,
            effective_sample, effective_tool,
            tmp_dir, data_root,
        )

        run_out = run_pytest(
            tests_dir, controller_dir, tmp_dir, effective_tool, project_root
        )

        if run_out["junit_xml"]:
            record.update(parse_junit_xml(run_out["junit_xml"]))
        else:
            record.update({
                "pass_count": 0, "fail_count": 0, "error_count": 0,
                "skip_count": 0, "total_count": 0, "pass_rate": 0.0,
                "test_cases": [],
                "runner_error": (run_out["stderr"] or run_out["stdout"] or "")[:2000],
            })

        if run_out["cov_json"]:
            cov = parse_coverage_json(run_out["cov_json"])
            if cov:
                record["coverage"] = cov

        record["pytest_returncode"] = run_out["returncode"]

    if output_file:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "a", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")

    return record


# ── CLI ────────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Measure test pass rate and coverage for a (controller, test) pair.\n\n"
            "Controller eval: pass a generated controller folder + ground-truth tests.\n"
            "Test eval      : pass a ground-truth controller folder + generated tests."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--controller", required=True, type=Path,
        metavar="DIR",
        help="Folder containing controller.py to evaluate.",
    )
    parser.add_argument(
        "--tests", required=True, type=Path,
        metavar="DIR",
        help="Folder containing the test files to run.",
    )
    parser.add_argument(
        "--output", type=Path, default=None,
        metavar="FILE.jsonl",
        help="Append result as a JSONL line to this file. Prints JSON to stdout if omitted.",
    )
    parser.add_argument(
        "--data-root", type=Path, default=DEFAULT_DATA_ROOT,
        metavar="DIR",
        help=f"Path to the data/ directory (default: {DEFAULT_DATA_ROOT}).",
    )
    parser.add_argument(
        "--sample", default=None,
        metavar="NAME",
        help="Sample name, e.g. AssetPlus (inferred from path if omitted).",
    )
    parser.add_argument(
        "--tool", default=None, choices=["ecore", "umple"],
        help="Modeling tool (inferred from path if omitted).",
    )
    args = parser.parse_args(argv)

    result = run_benchmark(
        controller_path=args.controller,
        test_path=args.tests,
        data_root=args.data_root,
        output_file=args.output,
        sample=args.sample,
        tool=args.tool,
    )

    if args.output:
        pr = result.get("pass_rate", 0.0)
        pc = result.get("pass_count", 0)
        tc = result.get("total_count", 0)
        print(f"Pass rate  : {pr:.1%}  ({pc}/{tc} tests)")
        cov = result.get("coverage", {})
        if "statement_coverage" in cov:
            print(f"Stmt cov   : {cov['statement_coverage']:.1%}")
        if "branch_coverage" in cov:
            print(f"Branch cov : {cov['branch_coverage']:.1%}")
        print(f"Written    : {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
