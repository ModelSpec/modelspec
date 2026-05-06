#!/usr/bin/env python3
"""
Grouped bar chart: average statement and branch coverage by prompt configuration.
Evaluates test generation results (eval_type == "test") run against
ground-truth controllers.

Configs prefixed with "feat_" include Gherkin feature scenarios in the prompt;
the others do not.  Groups: with features (feat_gen, feat_dom) vs without
features (gen, dom).

When --ref-file is provided (or the default reference_coverage.jsonl exists),
a dashed reference segment is drawn for each group at the human-reference level.

Usage
-----
    python -m tools.plots.coverage.config_coverage [--input FILE] [--output FILE] [--ref-file FILE]
"""

import argparse
from pathlib import Path

from .utils import (
    CONFIG_GROUP_LABELS,
    compute_averages,
    config_group,
    load_records,
    load_reference,
    plot,
    reference_overall,
)

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT   = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT  = Path(__file__).resolve().parent / "config_coverage.png"
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

    averages = compute_averages(records, key_fn=lambda r: config_group(r["config"]))

    ref_by_key = None
    if args.ref_file.exists():
        ref = load_reference(args.ref_file)
        overall = reference_overall(ref)
        ref_by_key = {k: overall for k in averages}
    else:
        print(f"Note: reference file not found ({args.ref_file}), skipping reference line.")

    print("Per-configuration-group coverage averages:")
    for group, (sm, _, bm, _) in sorted(averages.items(), key=lambda x: -x[1][0]):
        label = CONFIG_GROUP_LABELS.get(group, group)
        print(f"  {label:<30}  stmt {sm * 100:.2f}%  branch {bm * 100:.2f}%")

    plot(averages, CONFIG_GROUP_LABELS, xlabel="Prompt Configuration",
         output_file=args.output, ref_by_key=ref_by_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
