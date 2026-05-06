import argparse
from pathlib import Path
from typing import Any

from ..helper import analyze_model, clean_jsonl_per_sample, collect_samples, write_jsonl_per_sample
from ..helper import load_keyword_decisions, prompt_for_unknown_keywords, save_keyword_decisions

DEFAULT_JSONL_NAME = "domainmodel_attributes_metrics.jsonl"
DEFAULT_KEYWORDS_PATH = Path(__file__).resolve().parent / "reviewed_keywords.json"


def prepare_keyword_decisions(data_dir: Path, keywords_path: Path) -> dict[str, bool]:
    decisions = load_keyword_decisions(keywords_path)
    model_entries = collect_samples(data_dir)

    all_candidates: list[tuple[str, str]] = []
    for sample_name, model_path in model_entries:
        _, candidates, class_names, enum_names = analyze_model(model_path, decisions, sample_name)
        all_candidates.extend(candidates)
        for keyword, _ in candidates:
            if keyword in class_names or keyword in enum_names or keyword.endswith("[]"):
                decisions[keyword] = False

    prompt_for_unknown_keywords(decisions, all_candidates)
    save_keyword_decisions(keywords_path, decisions)
    return decisions


def compute_attribute_metrics(
    data_dir: Path, keywords_path: Path = DEFAULT_KEYWORDS_PATH
) -> list[dict[str, Any]]:
    decisions = prepare_keyword_decisions(data_dir, keywords_path)

    records: list[dict[str, Any]] = []
    for sample_name, model_path in collect_samples(data_dir):
        stats, _, _, _ = analyze_model(model_path, decisions, sample_name)
        records.append(
            {
                "sample": sample_name,
                "analyzer": "domainmodel.attributes",
                "metrics": {
                    "attributes": stats.attributes,
                },
            }
        )
    return records


def print_results(records: list[dict[str, Any]]) -> None:
    print("Analyzer: domainmodel.attributes")
    print(f"Records: {len(records)}\n")
    for record in records:
        metrics = record["metrics"]
        print(f"sample={record['sample']} |")
        print(f"  attributes: {metrics['attributes']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze attribute-level domain model metrics."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[4] / "data",
        help="Path to the data directory (default: repo/data)",
    )
    parser.add_argument(
        "--keywords-file",
        type=Path,
        default=DEFAULT_KEYWORDS_PATH,
        help="Path to reviewed keyword decisions JSON.",
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

    records = compute_attribute_metrics(args.data_dir, args.keywords_file)
    print_results(records)

    written_paths = write_jsonl_per_sample(output_dir, args.output_name, records)
    print(f"Wrote {len(written_paths)} sample file(s) under {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
