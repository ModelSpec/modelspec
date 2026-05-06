import argparse
import json
from pathlib import Path
from typing import Any

from .helper import iter_python_sources
from .full_metrics import build_method_reports, build_sample_report

DEFAULT_JSONL_STEM = "results"


def _sample_name_from_file(file_path: str, data_dir: Path) -> str:
    path = Path(file_path).resolve()
    for base in (data_dir.resolve(), (data_dir.parent / "results").resolve()):
        try:
            parts = path.relative_to(base).parts
            if parts:
                return parts[0]
        except ValueError:
            pass
    return path.parent.parent.parent.name if len(path.parts) >= 3 else path.parent.name


def _reports_from_sources(
    sources: list[tuple[Path, str]],
    metric: str,
    granularity: str,
) -> list[dict[str, Any]]:
    """Build metric reports from an explicit list of (path, source) pairs."""
    if granularity == "sample":
        full = [build_sample_report(p, s) for p, s in sources]
    else:
        full = [r for p, s in sources for r in build_method_reports(p, s)]

    if metric == "full":
        return full

    # core: keep only complexity + maintainability
    return [
        {
            "file_path": r["file_path"],
            **( {"method": r["method"]} if "method" in r else {} ),
            "cyclomatic_complexity": r["cyclomatic_complexity"],
            "maintainability_index": r["maintainability_index"],
        }
        for r in full
    ]


def _to_standard_records(
    reports: list[dict[str, Any]],
    data_dir: Path,
    benchmark_name: str,
) -> list[dict[str, Any]]:
    standardized: list[dict[str, Any]] = []
    for report in reports:
        file_path = str(report.get("file_path", ""))
        metrics = {
            **{
                key: value
                for key, value in report.items()
                if key not in {"file_path", "method"}
            },
        }

        record: dict[str, Any] = {
            "sample": _sample_name_from_file(file_path, data_dir),
            "benchmark": benchmark_name,
            "file_path": file_path,
            "metrics": metrics,
        }
        if "method" in report:
            record["method"] = report["method"]

        standardized.append(
            record
        )
    return standardized



def _default_jsonl_name(metric_mode: str, granularity: str) -> str:
    return f"{DEFAULT_JSONL_STEM}_{metric_mode}_{granularity}.jsonl"


def _resolve_output_path(output: Path, default_jsonl_name: str) -> Path:
    if output.exists() and output.is_dir():
        return output / default_jsonl_name
    if output.suffix.lower() != ".jsonl":
        return output / default_jsonl_name
    return output


def write_jsonl(output_path: Path, records: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False))
            file.write("\n")


def print_results(records: list[dict[str, Any]]) -> None:
    for record in records:
        metrics = record["metrics"]
        header = (
            f"sample={record['sample']} | "
            f"file_path={record['file_path']} |"
        )
        if "method" in record:
            header = (
                f"sample={record['sample']} | "
                f"file_path={record['file_path']} | "
                f"method={record['method']} |"
            )
        print(header)
        if "cyclomatic_complexity" in metrics:
            print(f"  cyclomatic_complexity={metrics['cyclomatic_complexity']}")
        if "maintainability_index" in metrics:
            print(f"  maintainability_index={metrics['maintainability_index']}")
        if "raw_metrics" in metrics:
            print(f"  raw_metrics={metrics['raw_metrics']}")
        if "halstead_metrics" in metrics:
            print(f"  halstead_metrics={metrics['halstead_metrics']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze Python files with Radon for software engineering metrics.",
    )
    parser.add_argument(
        "--controller",
        type=Path,
        required=True,
        metavar="DIR",
        help="Controller directory whose .py files are measured.",
    )
    parser.add_argument(
        "--metric",
        choices=["full", "core"],
        default="core",
        help="Metric mode: 'full' for all metrics, 'core' for complexity + maintainability only.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory for JSONL output (default: this folder)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=None,
        help=(
            "JSONL filename. Defaults to "
            "controller_complexity_results_<metric>_<granularity>.jsonl"
        ),
    )
    parser.add_argument(
        "--granularity",
        choices=["sample", "method"],
        default="method",
        help="Aggregation granularity: per file or per method.",
    )
    args = parser.parse_args()

    sources = iter_python_sources(args.controller)
    if not sources:
        print(f"No .py files found in {args.controller}")
        return 0

    default_output_name = _default_jsonl_name(args.metric, args.granularity)
    output_name = args.output_name or default_output_name
    output_path = _resolve_output_path(args.output_dir / output_name, default_output_name)

    print("Benchmark: controller.complexity")
    print(f"Controller : {args.controller}")
    print(f"Files      : {len(sources)}")
    print(f"Metric: {args.metric} | Granularity: {args.granularity}")
    print(f"JSONL output: {output_path.resolve()}")

    reports = _reports_from_sources(sources, args.metric, args.granularity)
    data_dir = Path(__file__).resolve().parents[3] / "data"
    standard = _to_standard_records(reports, data_dir, "controller.complexity")
    print(f"Records: {len(standard)}")
    print_results(standard)
    write_jsonl(output_path, standard)
    print(f"Saved JSONL results to: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
