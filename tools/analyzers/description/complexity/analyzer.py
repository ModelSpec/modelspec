import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import spacy
import textstat
from sentence_transformers import SentenceTransformer
from wordfreq import zipf_frequency
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_SENTENCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_SPACY_MODEL = "en_core_web_sm"
DEFAULT_PERPLEXITY_MODEL = "distilgpt2"
DEFAULT_JSONL_NAME = "description_complexity_metrics.jsonl"
COMPLEX_DEP_TAGS = {"mark", "advcl", "relcl", "ccomp"}


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


def dependency_tree_depth(token: Any, depth: int = 0) -> int:
    children = list(token.children)
    if not children:
        return depth
    return max(dependency_tree_depth(child, depth + 1) for child in children)


class PerplexityScorer:
    def __init__(self, model_name: str) -> None:
        try:
            import torch
        except ImportError as e:
            raise ImportError(
                f"This tool requires PyTorch (AKA torch) to run. See {Path(__file__).resolve().parent}/README.md for installation instructions, "
                "or run with --disable-perplexity."
            ) from e

        self._torch = torch
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForCausalLM.from_pretrained(model_name)
        self._model.eval()

    def score(self, text: str) -> float | None:
        encoded = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )
        if encoded["input_ids"].shape[1] < 2:
            return None

        with self._torch.no_grad():
            output = self._model(**encoded, labels=encoded["input_ids"])
            if output.loss is None:
                return None
            perplexity = self._torch.exp(output.loss).item()

        if math.isfinite(perplexity):
            return float(perplexity)
        return None


def analyze_sample(
    sample: SampleDescription,
    nlp: Any,
    sentence_model: Any,
    zipf_frequency: Any,
    textstat: Any,
    perplexity_scorer: PerplexityScorer | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "sample": sample.name,
        "analyzer": "description.complexity",
        "has_description": sample.description is not None,
    }

    if sample.description is None:
        result["error"] = "Missing description.txt or empty description."
        result["metrics"] = None
        return result

    text = sample.description
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    readability = {
        "flesch_kincaid_grade": float(textstat.flesch_kincaid_grade(text)),
        "dale_chall_score": float(textstat.dale_chall_readability_score(text)),
    }

    clause_count = sum(1 for token in doc if token.dep_ in COMPLEX_DEP_TAGS)
    sentence_depths = [dependency_tree_depth(sentence.root, 0) for sentence in doc.sents]
    syntactic = {
        "dependent_clause_count": clause_count,
        "max_grammatical_depth": max(sentence_depths) if sentence_depths else 0,
    }

    lexical_freqs: list[float] = []
    for token in doc:
        if token.is_punct or token.is_space or token.is_stop:
            continue
        lemma = token.lemma_.lower().strip()
        if not lemma:
            continue
        lexical_freqs.append(float(zipf_frequency(lemma, "en")))

    lexical = {
        "content_token_count": len(lexical_freqs),
        "average_zipf_frequency": (
            float(sum(lexical_freqs) / len(lexical_freqs)) if lexical_freqs else None
        ),
    }

    if len(sentences) <= 1:
        semantic = {
            "sentence_count": len(sentences),
            "pair_count": 0,
            "average_consecutive_similarity": 1.0,
        }
    else:
        embeddings = sentence_model.encode(
            sentences,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        similarities = [
            float(np.dot(embeddings[index], embeddings[index + 1]))
            for index in range(len(embeddings) - 1)
        ]
        semantic = {
            "sentence_count": len(sentences),
            "pair_count": len(similarities),
            "average_consecutive_similarity": float(
                sum(similarities) / len(similarities)
            ),
        }

    result["metrics"] = {
        "readability": readability,
        "syntactic": syntactic,
        "lexical": lexical,
        "semantic_cohesion": semantic,
    }

    if perplexity_scorer is not None:
        result["metrics"]["perplexity"] = perplexity_scorer.score(text)

    return result

def print_header() -> None:
    print("Metric guide:")
    print(
        "- readability: Estimates baseline reading difficulty from sentence length, word length, and common-word coverage."
    )
    print(
        "- syntactic: Estimates grammatical complexity using dependent clause count and maximum dependency-tree depth."
    )
    print(
        "- lexical: Estimates vocabulary sophistication using the average Zipf frequency of non-stopword content tokens."
    )
    print(
        "- semantic: Estimates coherence by averaging sentence-embedding similarity between consecutive sentences."
    )
    print(
        "- perplexity: Estimates how surprising the text is, where higher values usually indicate harder or less predictable text."
    )
    print("Evaluating samples...\n")


def print_results(records: list[dict[str, Any]]) -> None:
    print("Analyzer: description.complexity")
    print(f"Records: {len(records)}\n")
    for record in records:
        print(f"sample={record['sample']} |")
        if record["metrics"] is None:
            print(f"  status: {record['error']}")
            print()
            continue

        metrics = record["metrics"]
        readability = metrics["readability"]
        syntactic = metrics["syntactic"]
        lexical = metrics["lexical"]
        semantic = metrics["semantic_cohesion"]
        perplexity = metrics.get("perplexity", None)

        print(f"  readability.flesch_kincaid_grade: {readability['flesch_kincaid_grade']:.3f}")
        print(f"  readability.dale_chall_score: {readability['dale_chall_score']:.3f}")
        print(
            f"  syntactic.dependent_clause_count: {syntactic['dependent_clause_count']}"
        )
        print(f"  syntactic.max_grammatical_depth: {syntactic['max_grammatical_depth']}")
        avg_zipf = lexical["average_zipf_frequency"]
        avg_zipf_text = "None" if avg_zipf is None else f"{avg_zipf:.3f}"
        print(f"  lexical.content_token_count: {lexical['content_token_count']}")
        print(f"  lexical.average_zipf_frequency: {avg_zipf_text}")
        print(f"  semantic.sentence_count: {semantic['sentence_count']}")
        print(f"  semantic.pair_count: {semantic['pair_count']}")
        print(
            "  semantic.average_consecutive_similarity: "
            f"{semantic['average_consecutive_similarity']:.3f}"
        )
        perplexity_score = perplexity
        
        if perplexity_score is not None:
            print(f"  perplexity.score: {perplexity_score}")
        
        print()


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze cognitive text complexity for sample descriptions."
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
        help=f"JSONL file name (default: {DEFAULT_JSONL_NAME})",
    )
    parser.add_argument(
        "--sentence-model",
        type=str,
        default=DEFAULT_SENTENCE_MODEL,
        help="Sentence-transformers model for cohesion scoring.",
    )
    parser.add_argument(
        "--spacy-model",
        type=str,
        default=DEFAULT_SPACY_MODEL,
        help="spaCy model name for syntax and tokenization.",
    )
    parser.add_argument(
        "--perplexity-model",
        type=str,
        default=DEFAULT_PERPLEXITY_MODEL,
        help="Transformers causal LM model used for perplexity.",
    )
    parser.add_argument(
        "--disable-perplexity",
        action="store_true",
        help="Skip perplexity scoring.",
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

    sentence_model = SentenceTransformer(args.sentence_model)

    perplexity_scorer: PerplexityScorer | None = None
    if not args.disable_perplexity:
        try:
            perplexity_scorer = PerplexityScorer(args.perplexity_model)
        except Exception as error:
            print(
                f"Unable to initialize perplexity model '{args.perplexity_model}': {error}",
                file=sys.stderr,
            )

    try:
        nlp = spacy.load(args.spacy_model)
    except OSError as e:
        raise OSError(
            f"spaCy model is missing. Install it with: python -m spacy download {args.spacy_model}",
        ) from e

    print_header()

    samples = find_samples(args.data_dir)
    records = [
        analyze_sample(
            sample=sample,
            nlp=nlp,
            sentence_model=sentence_model,
            zipf_frequency=zipf_frequency,
            textstat=textstat,
            perplexity_scorer=perplexity_scorer,
        )
        for sample in samples
    ]

    print_results(records)

    written_paths = write_jsonl_per_sample(output_dir, args.output_name, records)
    print(f"Wrote {len(written_paths)} sample file(s) under: {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())