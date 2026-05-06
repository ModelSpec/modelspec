#!/usr/bin/env python3
"""
Compute average cyclomatic complexity for human-written ground-truth controllers.

For each (sample, tool) pair, analyzes data/{sample}/{tool}/controller/ and
records the avg_cyclomatic_complexity (average of per-method cyclomatic complexity).
Output is written as JSONL, one record per (sample, tool).

Usage
-----
    python -m tools.plots.complexity.compute_reference [--data-dir DIR] [--output FILE]
"""

import argparse
import json
import sys
from pathlib import Path

from .utils import SAMPLES

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "reference_complexity.jsonl"

TOOLS = ["ecore", "umple"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=DEFAULT_DATA_DIR, metavar="DIR",
        help=f"Ground-truth data directory (default: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT, metavar="FILE.jsonl",
        help=f"Output JSONL file (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args(argv)

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from tools.benchmarks.complexity.helper import iter_python_sources
    from tools.benchmarks.complexity.full_metrics import build_method_reports

    args.output.parent.mkdir(parents=True, exist_ok=True)
    total = len(SAMPLES) * len(TOOLS)
    done = 0

    with open(args.output, "w", encoding="utf-8") as out:
        for sample in SAMPLES:
            for tool in TOOLS:
                done += 1
                label = f"[{done}/{total}] {sample}/{tool}"
                controller_path = args.data_dir / sample / tool / "controller"
                try:
                    sources = list(iter_python_sources(controller_path))
                    ccs = []
                    for src_path, source in sources:
                        for m in build_method_reports(src_path, source):
                            ccs.append(m["cyclomatic_complexity"]["total"])
                    avg_cc = round(sum(ccs) / len(ccs), 4) if ccs else None
                    if avg_cc is None:
                        print(f"  {label}: no methods found")
                        continue
                    rec = {"sample": sample, "tool": tool, "avg_cyclomatic_complexity": avg_cc}
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    out.flush()
                    print(f"  {label}: avg_cc={avg_cc:.4f}")
                except Exception as exc:
                    print(f"  {label}: ERROR — {exc}")

    print(f"\nSaved -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
