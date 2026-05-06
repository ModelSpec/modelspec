#!/usr/bin/env python3
"""
Compute test coverage for human-written reference tests against ground-truth controllers.

For each (sample, tool) pair runs data/{sample}/tests/ against
data/{sample}/{tool}/controller/ and records statement and branch coverage.
Output is written as JSONL, one record per (sample, tool).

Usage
-----
    python -m tools.plots.coverage.compute_reference [--data-dir DIR] [--output FILE]
"""

import argparse
import json
import sys
from pathlib import Path

from .utils import SAMPLES

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "reference_coverage.jsonl"

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
    from tools.benchmarks.testpassrate.benchmark import run_benchmark

    args.output.parent.mkdir(parents=True, exist_ok=True)
    total = len(SAMPLES) * len(TOOLS)
    done = 0

    with open(args.output, "w", encoding="utf-8") as out:
        for sample in SAMPLES:
            for tool in TOOLS:
                done += 1
                label = f"[{done}/{total}] {sample}/{tool}"
                try:
                    result = run_benchmark(
                        controller_path=args.data_dir / sample / tool / "controller",
                        test_path=args.data_dir / sample / "tests",
                        data_root=args.data_dir,
                        output_file=None,
                        sample=sample,
                        tool=tool,
                        project_root=ROOT,
                    )
                    cov = result.get("coverage")
                    if not cov:
                        print(f"  {label}: no coverage data")
                        continue
                    rec = {"sample": sample, "tool": tool, **cov}
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    out.flush()
                    print(
                        f"  {label}: "
                        f"stmt={cov['statement_coverage']:.3f}  "
                        f"branch={cov['branch_coverage']:.3f}"
                    )
                except Exception as exc:
                    print(f"  {label}: ERROR — {exc}")

    print(f"\nSaved -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
