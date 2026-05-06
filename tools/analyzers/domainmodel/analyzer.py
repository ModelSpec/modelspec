import argparse
import importlib
from pathlib import Path
from typing import Any

from .attributes.analyzer import DEFAULT_KEYWORDS_PATH
from .attributes.analyzer import compute_attribute_metrics
from .file.analyzer import compute_file_metrics
from .relationships.analyzer import compute_relationship_metrics
from .helper import clean_jsonl_per_sample
from .helper import write_jsonl_per_sample
    

DEFAULT_JSONL_NAME = "domainmodel_metrics.jsonl"


def _compute_class_metrics(data_dir: Path) -> list[dict[str, Any]]:
    if __package__ in {None, ""}:
        class_module = importlib.import_module("domainmodels.class.analyzer")
    else:
        class_module = importlib.import_module(".class.analyzer", package=__package__)
    return class_module.compute_class_metrics(data_dir)


def _to_map(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {record["sample"]: record["metrics"] for record in records}


def compute_domainmodel_metrics(
    data_dir: Path,
    keywords_file: Path = DEFAULT_KEYWORDS_PATH,
) -> list[dict[str, Any]]:
    file_records = compute_file_metrics(data_dir)
    class_records = _compute_class_metrics(data_dir)
    relationship_records = compute_relationship_metrics(data_dir)
    attribute_records = compute_attribute_metrics(data_dir, keywords_file)

    file_by_sample = _to_map(file_records)
    class_by_sample = _to_map(class_records)
    rel_by_sample = _to_map(relationship_records)
    attr_by_sample = _to_map(attribute_records)

    sample_names = sorted(
        set(file_by_sample)
        | set(class_by_sample)
        | set(rel_by_sample)
        | set(attr_by_sample)
    )

    records: list[dict[str, Any]] = []
    for sample_name in sample_names:
        metrics = {}
        metrics.update(file_by_sample.get(sample_name, {}))
        metrics.update(class_by_sample.get(sample_name, {}))
        metrics.update(rel_by_sample.get(sample_name, {}))
        metrics.update(attr_by_sample.get(sample_name, {}))
        records.append(
            {
                "sample": sample_name,
                "analyzer": "domainmodel",
                "metrics": metrics,
            }
        )
    return records


def print_results(records: list[dict[str, Any]]) -> None:
    print("Analyzer: domainmodel")
    print(f"Records: {len(records)}\n")
    for record in records:
        metrics = record["metrics"]
        print(f"sample={record['sample']} |")
        print(f"  non_ws_chars: {metrics.get('non_ws_chars')}")
        print(f"  non_ws_lines: {metrics.get('non_ws_lines')}")
        print(f"  abstract_classes: {metrics.get('abstract_classes')}")
        print(f"  concrete_classes: {metrics.get('concrete_classes')}")
        print(f"  enums: {metrics.get('enums')}")
        print(f"  inheritance: {metrics.get('inheritance')}")
        print(f"  unidir_assoc: {metrics.get('unidir_assoc')}")
        print(f"  bidir_assoc: {metrics.get('bidir_assoc')}")
        print(f"  compositions: {metrics.get('compositions')}")
        print(f"  attributes: {metrics.get('attributes')}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze all domain model metrics by category."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "data",
        help="Path to the data directory (default: repo/data)",
    )
    parser.add_argument(
        "--keywords-file",
        type=Path,
        default=DEFAULT_KEYWORDS_PATH,
        help="Path to reviewed keyword decisions JSON (attributes analyzer).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for JSONL output (default: --data-dir)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=DEFAULT_JSONL_NAME,
        help=f"JSONL filename (default: {DEFAULT_JSONL_NAME})",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete generated output files and exit.",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or args.data_dir

    if args.clean:
        removed = clean_jsonl_per_sample(output_dir, args.output_name, args.data_dir)
        print(f"Removed {removed} file(s) for {args.output_name} under {output_dir}")
        return 0

    records = compute_domainmodel_metrics(args.data_dir, args.keywords_file)
    print_results(records)

    written_paths = write_jsonl_per_sample(output_dir, args.output_name, records)
    print(f"Wrote {len(written_paths)} sample file(s) under {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
