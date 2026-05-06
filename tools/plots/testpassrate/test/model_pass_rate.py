#!/usr/bin/env python3
"""
Bar chart: average test pass rate per model for test generation results.
Evaluates test generation results (eval_type == "test") run against
ground-truth controllers.

Usage
-----
    python -m tools.plots.testpassrate.test.model_pass_rate [--input FILE] [--output FILE]
"""

import argparse
from pathlib import Path

from ..utils import MODEL_LABELS, compute_averages, load_records, plot

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = ROOT / "pipeline_results.jsonl"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "model_pass_rate.png"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, metavar="FILE")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, metavar="FILE")
    args = parser.parse_args(argv)

    records = load_records(args.input, eval_type="test")
    if not records:
        print("No matching test test_pass_rate records found.")
        return 1

    averages = compute_averages(records, key_fn=lambda r: r["model"])
    print("Per-model averages:")
    for model, avg in sorted(averages.items(), key=lambda x: -x[1][0]):
        print(f"  {MODEL_LABELS.get(model, model):<25}  {avg[0] * 100:.2f}%  (std {avg[1] * 100:.2f}%)")

    plot(averages, MODEL_LABELS, xlabel="Model", output_file=args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
