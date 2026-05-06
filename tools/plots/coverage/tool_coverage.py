#!/usr/bin/env python3
"""
Grouped bar chart: average statement and branch coverage per modeling tool.
Evaluates test generation results (eval_type == "test") run against
ground-truth controllers.

When --ref-file is provided (or the default reference_coverage.jsonl exists),
a dashed reference segment is drawn per tool at its own human-reference level
(since the reference tests run against each tool's controller independently).

Usage
-----
    python -m tools.plots.coverage.tool_coverage [--input FILE] [--output FILE] [--ref-file FILE]
"""

import argparse
from pathlib import Path

from .utils import TOOL_LABELS, compute_averages, load_records, load_reference, plot

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT   = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT  = Path(__file__).resolve().parent / "tool_coverage.png"
DEFAULT_REF     = Path(__file__).resolve().parent / "reference_coverage.jsonl"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",    type=Path, default=DEFAULT_INPUT,  metavar="FILE")
    parser.add_argument("--output",   type=Path, default=DEFAULT_OUTPUT, metavar="FILE")
    parser.add_argument("--ref-file", type=Path, default=DEFAULT_REF,    metavar="FILE",
                        help="Reference coverage JSONL from compute_reference.py")
    args = parser.parse_args(argv)

    records = load_records(args.input)
    if not records:
        print("No matching test coverage records found.")
        return 1

    averages = compute_averages(records, key_fn=lambda r: r["tool"])

    # Per-tool reference: each tool's tests run against its own controller,
    # so the reference coverage differs between ecore and umple.
    ref_by_key = None
    if args.ref_file.exists():
        ref_by_key = load_reference(args.ref_file)
    else:
        print(f"Note: reference file not found ({args.ref_file}), skipping reference line.")

    print("Per-tool coverage averages:")
    for tool, (sm, _, bm, _) in sorted(averages.items(), key=lambda x: -x[1][0]):
        print(f"  {TOOL_LABELS.get(tool, tool):<10}  stmt {sm * 100:.2f}%  branch {bm * 100:.2f}%")

    plot(averages, TOOL_LABELS, xlabel="Modeling Tool",
         output_file=args.output, ref_by_key=ref_by_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
