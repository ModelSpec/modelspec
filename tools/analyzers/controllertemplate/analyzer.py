import argparse
import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_JSONL_NAME = "controller_template_metrics.jsonl"


@dataclass(frozen=True)
class ControllerMethodStats:
    sample: str
    method: str
    input_args: int


def find_controller_path(sample_dir: Path) -> Path | None:
    preferred = [
        sample_dir / "umple" / "controller" / "controller.py",
        sample_dir / "ecore" / "controller" / "controller.py",
    ]
    for path in preferred:
        if path.exists():
            return path

    matches = sorted(sample_dir.rglob("controller.py"))
    return matches[0] if matches else None


def count_method_args(method: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    args = method.args
    total = len(args.posonlyargs) + len(args.args) + len(args.kwonlyargs)
    if args.vararg is not None:
        total += 1
    if args.kwarg is not None:
        total += 1

    if args.args:
        first_arg = args.args[0].arg
        if first_arg in {"self", "cls"}:
            total -= 1
    elif args.posonlyargs:
        first_arg = args.posonlyargs[0].arg
        if first_arg in {"self", "cls"}:
            total -= 1

    return max(total, 0)


def compute_controller_template_metrics(data_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for child in sorted(data_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue

        controller_path = find_controller_path(child)
        if controller_path is None:
            continue

        try:
            text = controller_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(text)
        except (OSError, SyntaxError):
            continue

        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if item.name == "__init__" or item.name.startswith("_"):
                    continue

                stats = ControllerMethodStats(
                    sample=child.name,
                    method=item.name,
                    input_args=count_method_args(item),
                )
                records.append(
                    {
                        "sample": stats.sample,
                        "analyzer": "controllertemplate",
                        "entity": {
                            "method": stats.method,
                        },
                        "metrics": {
                            "input_args": stats.input_args,
                        },
                    }
                )

    return records


def write_jsonl(output_path: Path, records: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_jsonl_per_sample(
    output_dir: Path, output_name: str, records: list[dict[str, Any]]
) -> list[Path]:
    records_by_sample: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        sample_name = record.get("sample")
        if not isinstance(sample_name, str) or not sample_name:
            continue
        records_by_sample.setdefault(sample_name, []).append(record)

    written_paths: list[Path] = []
    for sample_name, sample_records in sorted(records_by_sample.items()):
        output_path = output_dir / sample_name / output_name
        write_jsonl(output_path, sample_records)
        written_paths.append(output_path)
    return written_paths


def clean_outputs(output_dir: Path, output_name: str, data_dir: Path) -> int:
    removed = 0
    for child in sorted(data_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue
        output_path = output_dir / child.name / output_name
        if output_path.exists():
            output_path.unlink()
            removed += 1
    print(f"Removed {removed} file(s) for {output_name} under {output_dir}")
    return 0


def print_results(records: list[dict[str, Any]]) -> None:
    print("Analyzer: controllertemplate")
    print(f"Records: {len(records)}\n")
    for record in records:
        print(
            f"sample={record['sample']} | "
            f"method={record['entity']['method']} |"
        )
        print(f"  input_args: {record['metrics']['input_args']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze controller templates and output per-method input argument counts."
        )
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "data",
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
        return clean_outputs(output_dir, args.output_name, args.data_dir)

    records = compute_controller_template_metrics(args.data_dir)
    print_results(records)

    written_paths = write_jsonl_per_sample(output_dir, args.output_name, records)
    print(f"\nWrote {len(written_paths)} sample file(s) under {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
