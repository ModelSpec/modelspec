import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AnalyzerRun:
    module: str
    argv: list[str]


def _to_cmdline(argv: list[str]) -> str:
    return subprocess.list2cmdline(argv)


def _shared_flags(args: argparse.Namespace) -> list[str]:
    flags = ["--data-dir", str(args.data_dir)]
    if args.output_dir is not None:
        flags.extend(["--output-dir", str(args.output_dir)])
    return flags


def build_runs(args: argparse.Namespace) -> list[AnalyzerRun]:
    shared = _shared_flags(args)
    clean_flag = ["--clean"] if args.clean else []
    runs: list[AnalyzerRun] = []

    runs.append(
        AnalyzerRun(
            module="controllertemplate.analyzer",
            argv=shared + ["--output-name", args.controller_output_name] + clean_flag,
        )
    )
    runs.append(
        AnalyzerRun(
            module="gherkin.analyzer",
            argv=shared + ["--output-name", args.gherkin_output_name] + clean_flag,
        )
    )
    runs.append(
        AnalyzerRun(
            module="domainmodel.analyzer",
            argv=shared
            + [
                "--keywords-file",
                str(args.keywords_file),
                "--output-name",
                args.domainmodel_output_name,
            ]
            + clean_flag,
        )
    )

    complexity_argv = shared + [
        "--output-name",
        args.description_complexity_output_name,
        "--sentence-model",
        args.sentence_model,
        "--spacy-model",
        args.spacy_model,
        "--perplexity-model",
        args.perplexity_model,
    ]
    if args.disable_perplexity:
        complexity_argv.append("--disable-perplexity")
    complexity_argv.extend(clean_flag)

    runs.append(
        AnalyzerRun(
            module="description.complexity.analyzer",
            argv=complexity_argv,
        )
    )

    if args.run_description_similarity:
        runs.append(
            AnalyzerRun(
                module="description.similarity.analyzer",
                argv=shared
                + [
                    "--output-name",
                    args.description_similarity_output_name,
                    "--model",
                    args.description_similarity_model,
                ]
                + clean_flag,
            )
        )

    return runs


def run_in_parallel(runs: list[AnalyzerRun], cwd: Path) -> int:
    if not runs:
        print("No analyzers selected.")
        return 0

    processes: list[tuple[AnalyzerRun, subprocess.Popen[str]]] = []
    python_exe = sys.executable

    for run in runs:
        command = _to_cmdline([python_exe, "-m", run.module, *run.argv])
        print(f"Starting: {command}", flush=True)
        process = subprocess.Popen(command, shell=True, cwd=str(cwd))
        processes.append((run, process))

    failures: list[tuple[str, int]] = []
    for run, process in processes:
        return_code = process.wait()
        if return_code != 0:
            failures.append((run.module, return_code))

    if failures:
        print("\nOne or more analyzers failed:", file=sys.stderr)
        for module, code in failures:
            print(f"- {module}: exit code {code}", file=sys.stderr)
        return 1

    print("\nAll analyzers completed successfully.")
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run top-level analyzers in parallel. "
            "Description similarity is skipped unless explicitly enabled."
        )
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data",
        help="Path to the data directory shared by all analyzers (default: repo/data).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Shared output root for all analyzers. "
            "If omitted, each analyzer uses its own default."
        ),
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Run all selected analyzers in clean mode to delete their outputs.",
    )

    parser.add_argument(
        "--controller-output-name",
        type=str,
        default="controller_template_metrics.jsonl",
        help="Output name for controllertemplate.analyzer.",
    )
    parser.add_argument(
        "--gherkin-output-name",
        type=str,
        default="gherkin_scenario_metrics.jsonl",
        help="Scenario output name for gherkin.analyzer.",
    )
    parser.add_argument(
        "--domainmodel-output-name",
        type=str,
        default="domainmodel_metrics.jsonl",
        help="Output name for domainmodel.analyzer.",
    )
    parser.add_argument(
        "--keywords-file",
        type=Path,
        default=(
            Path(__file__).resolve().parent
            / "domainmodel"
            / "attributes"
            / "reviewed_keywords.json"
        ),
        help="Keyword decisions JSON for domainmodel.analyzer.",
    )

    parser.add_argument(
        "--description-complexity-output-name",
        type=str,
        default="description_complexity_metrics.jsonl",
        help="Output name for description.complexity.analyzer.",
    )
    parser.add_argument(
        "--sentence-model",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence-transformers model for description complexity.",
    )
    parser.add_argument(
        "--spacy-model",
        type=str,
        default="en_core_web_sm",
        help="spaCy model for description complexity.",
    )
    parser.add_argument(
        "--perplexity-model",
        type=str,
        default="distilgpt2",
        help="Perplexity model for description complexity.",
    )
    parser.add_argument(
        "--disable-perplexity",
        action="store_true",
        help="Disable perplexity scoring in description complexity.",
    )

    parser.add_argument(
        "--run-description-similarity",
        action="store_true",
        help="Include description.similarity.analyzer (disabled by default).",
    )
    parser.add_argument(
        "--description-similarity-output-name",
        type=str,
        default="description_similarity_matrix.csv",
        help="Output name for description.similarity.analyzer.",
    )
    parser.add_argument(
        "--description-similarity-model",
        type=str,
        default="sentence-transformers/all-mpnet-base-v2",
        help="Model for description.similarity.analyzer.",
    )

    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()

    runs = build_runs(args)

    # TODO: produce one JSONL per sample with all metrics, instead of separate files per analyzer.
    return run_in_parallel(runs, cwd=Path(__file__).resolve().parent)


if __name__ == "__main__":
    raise SystemExit(main())
