import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

DEFAULT_INPUT = "description_complexity_metrics.jsonl"
DEFAULT_OUTPUT = "pearson_correlation_matrix.csv"


def is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def flatten_numeric_metrics(data: dict[str, Any], prefix: str = "") -> dict[str, float]:
    flattened: dict[str, float] = {}
    for key, value in data.items():
        name = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flattened.update(flatten_numeric_metrics(value, name))
        elif is_numeric(value):
            number = float(value)
            if math.isfinite(number):
                flattened[name] = number
    return flattened


def load_metric_rows(jsonl_path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with jsonl_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number} in {jsonl_path}: {error}"
                ) from error

            metrics = record.get("metrics")
            if not isinstance(metrics, dict):
                continue

            rows.append(flatten_numeric_metrics(metrics))

    return rows


def metric_names_from_rows(rows: list[dict[str, float]]) -> list[str]:
    names: set[str] = set()
    for row in rows:
        names.update(row.keys())
    return sorted(names)


def pearson_for_pair(
    rows: list[dict[str, float]], left: str, right: str
) -> float | None:
    left_values: list[float] = []
    right_values: list[float] = []

    for row in rows:
        left_value = row.get(left)
        right_value = row.get(right)
        if left_value is None or right_value is None:
            continue
        left_values.append(left_value)
        right_values.append(right_value)

    if len(left_values) < 2:
        return None

    x = np.array(left_values, dtype=float)
    y = np.array(right_values, dtype=float)

    if np.std(x) == 0.0 or np.std(y) == 0.0:
        if left == right:
            return 1.0
        return None

    value = float(np.corrcoef(x, y)[0, 1])
    if not math.isfinite(value):
        return None
    return value


def build_correlation_matrix(
    rows: list[dict[str, float]], metric_names: list[str]
) -> list[list[float | None]]:
    matrix: list[list[float | None]] = []
    for left in metric_names:
        row: list[float | None] = []
        for right in metric_names:
            correlation = pearson_for_pair(rows, left, right)
            row.append(correlation)
        matrix.append(row)
    return matrix


def write_csv(
    output_path: Path,
    metric_names: list[str],
    matrix: list[list[float | None]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric"] + metric_names)
        for metric_name, row in zip(metric_names, matrix):
            formatted = ["" if value is None else f"{value:.6f}" for value in row]
            writer.writerow([metric_name] + formatted)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute Pearson correlation matrix from complexity JSONL metrics."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path.cwd() / DEFAULT_INPUT,
        help=f"Path to complexity JSONL input (default: cwd/{DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory for CSV output (default: current working directory)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"CSV filename (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input JSONL not found: {args.input}")

    rows = load_metric_rows(args.input)
    if not rows:
        raise ValueError("No analyzable metrics found in input JSONL.")

    metric_names = metric_names_from_rows(rows)
    if not metric_names:
        raise ValueError("No numeric metrics found in input JSONL.")

    matrix = build_correlation_matrix(rows, metric_names)
    output_path = args.output_dir / args.output_name
    write_csv(output_path, metric_names, matrix)

    print(f"Loaded {len(rows)} analyzable samples from: {args.input}")
    print(f"Computed correlations for {len(metric_names)} metrics.")
    print(f"Wrote Pearson correlation matrix to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
