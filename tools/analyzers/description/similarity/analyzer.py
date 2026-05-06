import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/all-mpnet-base-v2"
DEFAULT_CSV_NAME = "description_similarity_matrix.csv"


@dataclass(frozen=True)
class SampleDescription:
    name: str
    description: str | None


def find_samples(data_dir: Path) -> list[SampleDescription]:
    samples: list[SampleDescription] = []
    for child in sorted(data_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue

        description_path = child / "description.txt"
        if not description_path.exists():
            samples.append(SampleDescription(name=child.name, description=None))
            continue

        text = description_path.read_text(encoding="utf-8", errors="replace").strip()
        samples.append(SampleDescription(name=child.name, description=text or None))

    return samples


def build_embeddings(
    samples: Iterable[SampleDescription], model_name: str
) -> dict[str, np.ndarray]:
    available = [sample for sample in samples if sample.description]
    if not available:
        return {}

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        sentences=[sample.description for sample in available if sample.description],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    return {sample.name: embeddings[index] for index, sample in enumerate(available)}


def build_similarity_matrix(
    sample_names: list[str], embeddings: dict[str, np.ndarray]
) -> list[list[float | None]]:
    matrix: list[list[float | None]] = []
    for row_name in sample_names:
        row: list[float | None] = []
        row_vec = embeddings.get(row_name)
        for col_name in sample_names:
            col_vec = embeddings.get(col_name)
            if row_vec is None or col_vec is None:
                row.append(None)
            else:
                row.append(float(np.dot(row_vec, col_vec)))
        matrix.append(row)
    return matrix


def write_csv_matrix(
    output_path: Path,
    sample_names: list[str],
    matrix: list[list[float | None]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sample"] + sample_names)
        for name, row in zip(sample_names, matrix):
            formatted_row = ["" if value is None else f"{value:.4f}" for value in row]
            writer.writerow([name] + formatted_row)


def print_results(sample_names: list[str], matrix: list[list[float | None]]) -> None:
    print("Analyzer: description.similarity")
    print(f"Rows: {len(sample_names)}")
    print(f"Columns: {len(sample_names)}")


def clean_output(output_path: Path) -> int:
    if output_path.exists():
        output_path.unlink()
        print(f"Removed CSV matrix: {output_path}")
    else:
        print(f"No output file to remove: {output_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare description.txt files with sentence-transformers."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[4] / "data",
        help="Path to the data directory (default: repo/data)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="Sentence-transformers model name or path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory for CSV output (default: this folder)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=DEFAULT_CSV_NAME,
        help=f"CSV filename (default: {DEFAULT_CSV_NAME})",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete generated output CSV and exit.",
    )
    args = parser.parse_args()
    output_path = args.output_dir / args.output_name

    if args.clean:
        return clean_output(output_path)

    samples = find_samples(args.data_dir)
    embeddings = build_embeddings(samples, args.model)
    sample_names = [sample.name for sample in samples]
    matrix = build_similarity_matrix(sample_names, embeddings)

    write_csv_matrix(output_path, sample_names, matrix)
    print_results(sample_names, matrix)
    print(f"Wrote CSV matrix to: {output_path}")

    missing = [sample.name for sample in samples if sample.description is None]
    if missing:
        print(
            "Missing description.txt for: " + ", ".join(missing),
            file=sys.stderr,
            flush=True,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
