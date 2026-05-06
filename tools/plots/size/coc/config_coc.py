#!/usr/bin/env python3
"""
Bar chart: average characters of code by prompt configuration (controller eval).

Usage
-----
    python -m tools.plots.size.coc.config_coc [--input FILE] [--output FILE] [--ref-file FILE]
"""

import argparse
from pathlib import Path

from ..utils import (
    CONFIG_GROUP_LABELS,
    compute_averages,
    config_group,
    load_records,
    load_reference,
    plot,
    reference_overall,
)

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT  = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "config_coc.png"
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

    averages = compute_averages(records, key_fn=lambda r: config_group(r["config"]))

    ref_by_key = None
    if args.ref_file.exists():
        ref = load_reference(args.ref_file)
        overall = reference_overall(ref)
        ref_by_key = {k: overall for k in averages}
    else:
        print(f"Note: reference file not found ({args.ref_file}), skipping reference line.")

    print("Per-configuration-group characters-of-code averages:")
    for group, (_lm, _, cm, _) in sorted(averages.items(), key=lambda x: x[1][2]):
        label = CONFIG_GROUP_LABELS.get(group, group)
        print(f"  {label:<30}  chars {cm:.1f}")

    plot(averages, CONFIG_GROUP_LABELS, xlabel="Prompt Configuration",
         ylabel="Characters of Code", output_file=args.output,
         metric="chars", ref_by_key=ref_by_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
