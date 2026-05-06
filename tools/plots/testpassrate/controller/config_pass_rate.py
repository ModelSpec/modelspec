#!/usr/bin/env python3
"""
Bar chart: average test pass rate by prompt configuration, LLM-agnostic.
Evaluates controller generation results (eval_type == "controller").

Configs prefixed with "feat_" include Gherkin feature scenarios in the prompt;
the others do not.  Groups: with features (feat_gen, feat_dom) vs without
features (gen, dom).

Usage
-----
    python -m tools.plots.testpassrate.controller.config_pass_rate [--input FILE] [--output FILE]
"""

import argparse
from pathlib import Path

from ..utils import (
    CONFIG_GROUP_LABELS,
    compute_averages,
    config_group,
    load_records,
    plot,
)

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "config_pass_rate.png"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, metavar="FILE")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, metavar="FILE")
    args = parser.parse_args(argv)

    records = load_records(args.input, eval_type="controller")
    if not records:
        print("No matching controller test_pass_rate records found.")
        return 1

    averages = compute_averages(records, key_fn=lambda r: config_group(r["config"]))
    print("Per-configuration-group averages:")
    for group, avg in sorted(averages.items(), key=lambda x: -x[1][0]):
        label = CONFIG_GROUP_LABELS.get(group, group)
        print(f"  {label:<30}  {avg[0] * 100:.2f}%  (std {avg[1] * 100:.2f}%)")

    plot(averages, CONFIG_GROUP_LABELS, xlabel="Prompt Configuration", output_file=args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
