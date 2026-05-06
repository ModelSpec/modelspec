import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Iterable

CLASS_NAME_RE = re.compile(r"^\s*(?:class|associationClass)\s+([A-Za-z_][\w]*)\b")
ENUM_NAME_RE = re.compile(r"^\s*enum\s+([A-Za-z_][\w]*)\b")
ABSTRACT_RE = re.compile(r"^\s*abstract\b")
ISA_RE = re.compile(r"^\s*isA\b")
UNIDIR_RE = re.compile(r"<-|->")
BIDIR_RE = re.compile(r"--")
COMPOSITION_RE = re.compile(r"<@>-|-<@>")
MULTIPLICITY_RE = re.compile(r"^\s*(\*|\d+)(?:\.\.(\*|\d+))?(?=\s|$)")
ATTRIBUTE_NAME_RE = re.compile(r"^[A-Za-z_][\w]*$")
ATTRIBUTE_TYPE_RE = re.compile(r"^[A-Za-z_][\w\.\[\]]*$")


@dataclass
class DomainModelStats:
    name: str
    model_path: Path
    non_ws_chars: int = 0
    non_ws_lines: int = 0
    classes: int = 0
    abstract_classes: int = 0
    enums: int = 0
    inheritance: int = 0
    unidir_assoc: int = 0
    bidir_assoc: int = 0
    compositions: int = 0
    attributes: int = 0

    @property
    def concrete_classes(self) -> int:
        return self.classes - self.abstract_classes


def load_keyword_decisions(path: Path) -> dict[str, bool]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    keywords = data.get("keywords", {})
    return {str(k): bool(v) for k, v in keywords.items()}


def save_keyword_decisions(path: Path, decisions: dict[str, bool]) -> None:
    data = {"keywords": dict(sorted(decisions.items()))}
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def strip_comments(lines: Iterable[str]) -> Iterable[str]:
    in_block = False
    for line in lines:
        working = line
        if in_block:
            end = working.find("*/")
            if end == -1:
                yield ""
                continue
            working = working[end + 2 :]
            in_block = False

        while True:
            start = working.find("/*")
            if start == -1:
                break
            end = working.find("*/", start + 2)
            if end == -1:
                working = working[:start]
                in_block = True
                break
            working = working[:start] + working[end + 2 :]

        if "//" in working:
            working = working.split("//", 1)[0]
        yield working


def parse_attribute_line(line: str) -> tuple[bool, tuple[str, str] | None]:
    stripped = line.strip()
    if not stripped.endswith(";"):
        return False, None

    body = stripped[:-1].strip()
    if not body:
        return False, None

    parts = body.split()
    if not parts:
        return False, None

    name = parts[-1]

    if len(parts) == 1:
        if not ATTRIBUTE_NAME_RE.match(name):
            return False, None
        return True, None

    if not ATTRIBUTE_TYPE_RE.match(name):
        return False, None

    return False, (parts[0], name)


def analyze_model(
    model_path: Path, keyword_decisions: dict[str, bool], sample_name: str
) -> tuple[DomainModelStats, list[tuple[str, str]], set[str], set[str]]:
    text = model_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    stats = DomainModelStats(name=sample_name, model_path=model_path)

    stats.non_ws_chars = sum(1 for ch in text if not ch.isspace())
    stats.non_ws_lines = sum(1 for line in lines if line.strip())

    attribute_candidates: list[tuple[str, str]] = []
    class_names: set[str] = set()
    enum_names: set[str] = set()

    for line in strip_comments(lines):
        stripped = line.strip()
        if not stripped:
            continue

        matched_structural = False

        class_match = CLASS_NAME_RE.match(stripped)
        if class_match:
            stats.classes += 1
            class_names.add(class_match.group(1))
            matched_structural = True
        if ABSTRACT_RE.match(stripped):
            stats.abstract_classes += 1
            matched_structural = True
        enum_match = ENUM_NAME_RE.match(stripped)
        if enum_match:
            stats.enums += 1
            enum_names.add(enum_match.group(1))
            matched_structural = True
        if ISA_RE.match(stripped):
            stats.inheritance += 1
            matched_structural = True

        if COMPOSITION_RE.search(stripped):
            stats.compositions += len(COMPOSITION_RE.findall(stripped))
            matched_structural = True

        unidir_hits = UNIDIR_RE.findall(stripped)
        if unidir_hits:
            stats.unidir_assoc += len(unidir_hits)
            matched_structural = True

        if BIDIR_RE.search(stripped):
            stats.bidir_assoc += len(BIDIR_RE.findall(stripped))
            matched_structural = True
        else:
            has_connectors = any(
                token in stripped
                for token in ("--", "<-", "->", "<@>-", "-<@>")
            )
            if not has_connectors and MULTIPLICITY_RE.match(stripped):
                stats.bidir_assoc += 1
                matched_structural = True

        if not matched_structural:
            is_single, candidate = parse_attribute_line(stripped)
            if is_single:
                stats.attributes += 1
            elif candidate is not None:
                attribute_candidates.append(candidate)

    for keyword, _ in attribute_candidates:
        if keyword_decisions.get(keyword) is False:
            stats.attributes += 1

    return stats, attribute_candidates, class_names, enum_names


def collect_samples(data_dir: Path) -> list[tuple[str, Path]]:
    samples: list[tuple[str, Path]] = []
    for child in sorted(data_dir.iterdir()):
        if not child.is_dir():
            continue
        model_path = child / "umple" / "model" / "model.ump"
        if model_path.exists():
            samples.append((child.name, model_path))
            continue
        matches = sorted(child.rglob("model.ump"))
        if matches:
            samples.append((child.name, matches[0]))
    return samples


def prompt_for_unknown_keywords(
    decisions: dict[str, bool], candidates: Iterable[tuple[str, str]]
) -> None:
    candidates_list = list(candidates)
    keywords = {kw for kw, _ in candidates_list}
    unknown = sorted({kw for kw in keywords if kw not in decisions})
    if not unknown:
        return

    print("\nReview attribute keywords. Mark reserved keywords as 'y'.")
    for keyword in unknown:
        while True:
            example = next(
                (f"{kw} {name};" for kw, name in candidates_list if kw == keyword),
                None,
            )
            response = (
                input(f"Is '{keyword}' in '{example}' reserved? [y/n]: ")
                .strip()
                .lower()
            )
            if response in {"y", "n"}:
                decisions[keyword] = response == "y"
                break
            print("Please answer with 'y' or 'n'.")


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


def clean_jsonl_per_sample(output_dir: Path, output_name: str, data_dir: Path) -> int:
    removed = 0
    for child in sorted(data_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue
        output_path = output_dir / child.name / output_name
        if output_path.exists():
            output_path.unlink()
            removed += 1
    return removed
