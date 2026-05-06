import argparse
import json
import re
from pathlib import Path
from typing import Any

SCENARIO_RE = re.compile(r"^\s*Scenario:\s+(?P<name>.+?)\s*$")
SCENARIO_OUTLINE_RE = re.compile(r"^\s*Scenario Outline:\s+(?P<name>.+?)\s*$")
BACKGROUND_RE = re.compile(r"^\s*Background:\s*(?P<name>.*)$")
EXAMPLES_RE = re.compile(r"^\s*Examples?:\s*")
STEP_RE = re.compile(r"^\s*(Given|When|Then|And|But)\b")
FAILURE_RE = re.compile(r"\b(error|exception|failure|fail)\b", re.IGNORECASE)
NEGATED_FAILURE_RE = re.compile(r"\bno\s+(error|exception)\b", re.IGNORECASE)
THROW_RAISE_RE = re.compile(r"\b(throw|raise)\b", re.IGNORECASE)
NOT_THROW_RAISE_RE = re.compile(r"\bnot\s+(throw|raise)\b", re.IGNORECASE)
DEFAULT_JSONL_NAME = "gherkin_scenario_metrics.jsonl"
DEFAULT_BACKGROUND_JSONL_NAME = "gherkin_background_metrics.jsonl"


def _new_step_counter() -> dict[str, int]:
    return {"given": 0, "when": 0, "then": 0}


def _resolve_background_output_path(output_path: Path) -> Path:
    return output_path.with_name(DEFAULT_BACKGROUND_JSONL_NAME)


def parse_feature_file(path: Path, sample_name: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    records: list[dict[str, Any]] = []

    current_name: str | None = None
    current_is_outline = False
    current_has_failure = False
    current_steps = _new_step_counter()
    current_last_primary_step: str | None = None

    in_examples = False
    example_has_header = False
    outline_rows = 0

    in_background = False
    background_given_steps = 0
    background_last_primary_step: str | None = None
    pending_given_scope: str | None = None
    pending_given_has_header = False
    pending_given_rows = 0
    feature_name = path.stem

    def start_pending_given_table(scope: str) -> None:
        nonlocal pending_given_scope, pending_given_has_header, pending_given_rows
        pending_given_scope = scope
        pending_given_has_header = False
        pending_given_rows = 0

    def close_pending_given_table() -> None:
        nonlocal pending_given_scope, pending_given_has_header, pending_given_rows
        nonlocal current_steps, background_given_steps
        if pending_given_scope is None:
            return
        if pending_given_rows > 0:
            adjustment = pending_given_rows - 1
            if pending_given_scope == "scenario":
                current_steps["given"] += adjustment
            else:
                background_given_steps += adjustment
        pending_given_scope = None
        pending_given_has_header = False
        pending_given_rows = 0

    def close_current() -> None:
        nonlocal current_name, current_is_outline, current_has_failure
        nonlocal current_steps, current_last_primary_step
        nonlocal in_examples, example_has_header, outline_rows
        close_pending_given_table()

        if current_name is None:
            return

        scenario_count = outline_rows if current_is_outline else 1
        records.append(
            {
                "sample": sample_name,
                "analyzer": "gherkin.scenario",
                "entity": {
                    "feature": feature_name,
                    "scenario": current_name,
                },
                "metrics": {
                    "scenario_count": scenario_count,
                    "is_success_scenario": not current_has_failure,
                    "given_steps": current_steps["given"],
                    "when_steps": current_steps["when"],
                    "then_steps": current_steps["then"],
                },
            }
        )

        current_name = None
        current_is_outline = False
        current_has_failure = False
        current_steps = _new_step_counter()
        current_last_primary_step = None
        in_examples = False
        example_has_header = False
        outline_rows = 0

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            close_pending_given_table()
            if in_examples and not stripped:
                in_examples = False
                example_has_header = False
            continue

        outline_match = SCENARIO_OUTLINE_RE.match(stripped)
        if outline_match:
            close_current()
            current_name = outline_match.group("name")
            current_is_outline = True
            in_background = False
            continue

        scenario_match = SCENARIO_RE.match(stripped)
        if scenario_match:
            close_current()
            current_name = scenario_match.group("name")
            current_is_outline = False
            in_background = False
            continue

        background_match = BACKGROUND_RE.match(stripped)
        if background_match:
            close_current()
            in_background = True
            background_last_primary_step = None
            continue

        step_match = STEP_RE.match(stripped)

        if pending_given_scope is not None and "|" in stripped:
            if not pending_given_has_header:
                pending_given_has_header = True
            else:
                pending_given_rows += 1
            continue

        close_pending_given_table()

        if current_name is None:
            if in_background and step_match:
                keyword = step_match.group(1)
                if keyword == "Given":
                    background_given_steps += 1
                    background_last_primary_step = "given"
                    start_pending_given_table("background")
                elif keyword == "When":
                    background_last_primary_step = "when"
                elif keyword == "Then":
                    background_last_primary_step = "then"
                elif keyword in {"And", "But"} and background_last_primary_step == "given":
                    background_given_steps += 1
                    start_pending_given_table("background")
            continue

        if current_is_outline and EXAMPLES_RE.match(stripped):
            in_examples = True
            example_has_header = False
            continue

        if in_examples:
            if "|" in stripped:
                if not example_has_header:
                    example_has_header = True
                else:
                    outline_rows += 1
            else:
                in_examples = False
                example_has_header = False

        if step_match:
            keyword = step_match.group(1)
            effective_step_type: str | None = None

            if keyword == "Given":
                current_steps["given"] += 1
                current_last_primary_step = "given"
                effective_step_type = "given"
                start_pending_given_table("scenario")
            elif keyword == "When":
                current_steps["when"] += 1
                current_last_primary_step = "when"
                effective_step_type = "when"
            elif keyword == "Then":
                current_steps["then"] += 1
                current_last_primary_step = "then"
                effective_step_type = "then"
            elif keyword in {"And", "But"} and current_last_primary_step is not None:
                current_steps[current_last_primary_step] += 1
                effective_step_type = current_last_primary_step
                if current_last_primary_step == "given":
                    start_pending_given_table("scenario")

            if effective_step_type == "then":
                has_failure_keyword = FAILURE_RE.search(stripped) is not None
                has_negated_failure = NEGATED_FAILURE_RE.search(stripped) is not None
                has_throw_raise = THROW_RAISE_RE.search(stripped) is not None
                has_not_throw_raise = NOT_THROW_RAISE_RE.search(stripped) is not None
                has_failure_signal = has_failure_keyword or (has_throw_raise and not has_not_throw_raise)
                if has_failure_signal and not has_negated_failure and not has_not_throw_raise:
                    current_has_failure = True

    close_current()
    close_pending_given_table()
    background_record = {
        "sample": sample_name,
        "analyzer": "gherkin.background",
        "entity": {
            "feature": feature_name,
        },
        "metrics": {
            "background_given_steps": background_given_steps,
        },
    }
    return records, background_record


def compute_gherkin_metrics(data_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scenario_records: list[dict[str, Any]] = []
    background_records: list[dict[str, Any]] = []

    for child in sorted(data_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue

        features_dir = child / "features"
        if not features_dir.exists():
            continue

        for feature_file in sorted(features_dir.rglob("*.feature")):
            file_scenario_records, file_background_record = parse_feature_file(
                feature_file, child.name
            )
            scenario_records.extend(file_scenario_records)
            background_records.append(file_background_record)

    return scenario_records, background_records


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
    background_output_name = _resolve_background_output_path(Path(output_name)).name
    removed = 0
    for child in sorted(data_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue
        for name in (output_name, background_output_name):
            output_path = output_dir / child.name / name
            if output_path.exists():
                output_path.unlink()
                removed += 1
    print(f"Removed {removed} file(s) for {output_name} under {output_dir}")
    return 0


def print_scenario_results(records: list[dict[str, Any]]) -> None:
    print("Analyzer: gherkin.scenario")
    print(f"Records: {len(records)}\n")
    for record in records:
        metrics = record["metrics"]
        print(
            f"sample={record['sample']} | "
            f"feature={record['entity']['feature']} | "
            f"scenario={record['entity']['scenario']} |"
        )
        print(f"  is_success_scenario={str(metrics['is_success_scenario']).lower()}")
        print(f"  scenario_count={metrics['scenario_count']}")
        print(f"  Given={metrics['given_steps']}")
        print(f"  When={metrics['when_steps']}")
        print(f"  Then={metrics['then_steps']}")
        print()


def print_background_results(records: list[dict[str, Any]]) -> None:
    print("\nAnalyzer: gherkin.background")
    print(f"Records: {len(records)}\n")
    for record in records:
        print(
            f"sample={record['sample']} | "
            f"feature={record['entity']['feature']} | "
            "background |"
        )
        print(f"  background_Given={record['metrics']['background_given_steps']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze Gherkin feature files into per-scenario statistics."
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
        help=f"Scenario JSONL filename (default: {DEFAULT_JSONL_NAME})",
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

    scenario_records, background_records = compute_gherkin_metrics(args.data_dir)
    print_scenario_results(scenario_records)
    print_background_results(background_records)

    background_output_name = _resolve_background_output_path(Path(args.output_name)).name
    scenario_paths = write_jsonl_per_sample(output_dir, args.output_name, scenario_records)
    background_paths = write_jsonl_per_sample(
        output_dir,
        background_output_name,
        background_records,
    )
    print(f"\nSaved {len(scenario_paths)} scenario sample file(s) under: {output_dir.resolve()}")
    print(f"Saved {len(background_paths)} background sample file(s) under: {output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
