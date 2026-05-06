#!/usr/bin/env python3
"""
Bar chart: average lines of code per modeling tool (controller eval).

Usage
-----
    python -m tools.plots.size.loc.tool_loc [--input FILE] [--output FILE] [--ref-file FILE]
"""

import argparse
from pathlib import Path

from ..utils import TOOL_LABELS, compute_averages, load_records, load_reference, plot

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT  = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "tool_loc.png"
DEFAULT_REF    = Path(__file__).resolve().parents[1] / "reference_size.jsonl"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",    type=Path, default=DEFAULT_INPUT,  metavar="FILE")
    parser.add_argument("--output",   type=Path, default=DEFAULT_OUTPUT, metavar="FILE")
    parser.add_argument("--ref-file", type=Path, default=DEFAULT_REF,    metavar="FILE")
    args = parser.parse_args(argv)

    records = load_records(args.input)
    if not records:
        print("No matching code size records found.")
        return 1

    averages = compute_averages(records, key_fn=lambda r: r["tool"])

    ref_by_key = None
    if args.ref_file.exists():
        ref_by_key = load_reference(args.ref_file)
    else:
        print(f"Note: reference file not found ({args.ref_file}), skipping reference line.")

    print("Per-tool lines-of-code averages:")
    for tool, (lm, _, _cm, _) in sorted(averages.items(), key=lambda x: x[1][0]):
        print(f"  {TOOL_LABELS.get(tool, tool):<10}  loc {lm:.1f}")

    plot(averages, TOOL_LABELS, xlabel="Modeling Tool",
         ylabel="Lines of Code", output_file=args.output,
         metric="loc", ref_by_key=ref_by_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
