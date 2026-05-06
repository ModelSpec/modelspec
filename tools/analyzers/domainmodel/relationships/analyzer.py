import argparse
from pathlib import Path
from typing import Any

from ..helper import analyze_model, clean_jsonl_per_sample, collect_samples, write_jsonl_per_sample

DEFAULT_JSONL_NAME = "domainmodel_relationships_metrics.jsonl"


def compute_relationship_metrics(data_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for sample_name, model_path in collect_samples(data_dir):
        stats, _, _, _ = analyze_model(model_path, {}, sample_name)
        records.append(
            {
                "sample": sample_name,
                "analyzer": "domainmodel.relationships",
                "metrics": {
                    "inheritance": stats.inheritance,
                    "unidir_assoc": stats.unidir_assoc,
                    "bidir_assoc": stats.bidir_assoc,
                    "compositions": stats.compositions,
                },
            }
        )
    return records


def print_results(records: list[dict[str, Any]]) -> None:
    print("Analyzer: domainmodel.relationships")
    print(f"Records: {len(records)}\n")
    for record in records:
        metrics = record["metrics"]
        print(f"sample={record['sample']} |")
        print(f"  inheritance: {metrics['inheritance']}")
        print(f"  unidir_assoc: {metrics['unidir_assoc']}")
        print(f"  bidir_assoc: {metrics['bidir_assoc']}")
        print(f"  compositions: {metrics['compositions']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze relationship-level domain model metrics."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[4] / "data",
        help="Path to the data directory (default: repo/data)",
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

    records = compute_relationship_metrics(args.data_dir)
    print_results(records)

    written_paths = write_jsonl_per_sample(output_dir, args.output_name, records)
    print(f"Wrote {len(written_paths)} sample file(s) under {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
