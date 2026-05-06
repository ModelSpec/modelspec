#!/usr/bin/env python3
"""
Bar chart: average cyclomatic complexity per modeling tool (controller eval).

Bars grow from top to bottom — lower complexity is better.

When --ref-file is provided (or the default reference_complexity.jsonl exists),
a reference line is drawn per tool at its own human-reference complexity level
(since each tool's ground-truth controller has an independent baseline).

Usage
-----
    python -m tools.plots.complexity.tool_complexity [--input FILE] [--output FILE] [--ref-file FILE]
"""

import argparse
from pathlib import Path

from .utils import TOOL_LABELS, compute_averages, load_records, load_reference, plot

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT  = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "tool_complexity.png"
DEFAULT_REF    = Path(__file__).resolve().parent / "reference_complexity.jsonl"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",    type=Path, default=DEFAULT_INPUT,  metavar="FILE")
    parser.add_argument("--output",   type=Path, default=DEFAULT_OUTPUT, metavar="FILE")
    parser.add_argument("--ref-file", type=Path, default=DEFAULT_REF,    metavar="FILE",
                        help="Reference complexity JSONL from compute_reference.py")
    args = parser.parse_args(argv)

    records = load_records(args.input)
    if not records:
        print("No matching complexity records found.")
        return 1

    averages = compute_averages(records, key_fn=lambda r: r["tool"])

    # Per-tool reference: each tool's controller has its own complexity baseline.
    ref_by_key = None
    if args.ref_file.exists():
        ref_by_key = load_reference(args.ref_file)
    else:
        print(f"Note: reference file not found ({args.ref_file}), skipping reference line.")

    print("Per-tool complexity averages:")
    for tool, (mean, _) in sorted(averages.items(), key=lambda x: x[1][0]):
        print(f"  {TOOL_LABELS.get(tool, tool):<10}  avg_cc {mean:.4f}")

    plot(averages, TOOL_LABELS, xlabel="Modeling Tool",
         output_file=args.output, ref_by_key=ref_by_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
