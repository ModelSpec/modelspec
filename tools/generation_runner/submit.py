"""
tools/generation_runner/submit.py

CLI entry point for submitting generation batch jobs.  Delegates prompt
building to the mode-specific submodule (controller/ or test/) and uses
shared infrastructure for API submission and batch tracking.

Usage:
    python -m tools.generation_runner.submit controller                                   # all models, all tools, all configs, all samples
    python -m tools.generation_runner.submit test gpt-5.4-nano                            # one model, all tools, all configs, all samples
    python -m tools.generation_runner.submit controller claude-haiku-4-5 --tool umple
    python -m tools.generation_runner.submit test --tool ecore --config feat_gen --config gen
    python -m tools.generation_runner.submit controller --sample BusTransportationManagementSystem
    python -m tools.generation_runner.submit controller --sample Foo --sample Bar
    python -m tools.generation_runner.submit controller --repetitions 5
"""

import argparse

from ._shared import (
    DEFAULT_MODELS, ALL_TOOLS, ALL_CONFIGS, ALL_MODES,
    PROVIDERS, make_client, save_batch_info, api_for_model, discover_samples,
)
from .controller.submit import build_requests as build_controller_requests
from .test.submit import build_requests as build_test_requests

_BUILDERS = {
    "controller": build_controller_requests,
    "test": build_test_requests,
}


def _parse_args() -> tuple[str, list[str], list[str], list[str], list[str], int]:
    """Return (mode, models, tools, configs, samples, repetitions) from command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Submit generation batch jobs (controller or test).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mode",
        choices=ALL_MODES,
        help="Generation mode: 'controller' to generate implementations, "
             "'test' to generate pytest test files.",
    )
    parser.add_argument(
        "models",
        nargs="*",
        default=DEFAULT_MODELS,
        metavar="MODEL",
        help=f"Model names to submit (default: {DEFAULT_MODELS})",
    )
    parser.add_argument(
        "--tool", "-t",
        dest="tools",
        action="append",
        choices=ALL_TOOLS,
        metavar="TOOL",
        help=f"Tool to include: {ALL_TOOLS}. May be repeated. Defaults to all tools.",
    )
    parser.add_argument(
        "--config", "-c",
        dest="configs",
        action="append",
        choices=ALL_CONFIGS,
        metavar="CONFIG",
        help=(
            f"Config to include: {ALL_CONFIGS}. May be repeated. "
            "Defaults to all configs. "
            "feat_gen=description+features+generated model layer, "
            "gen=description+generated model layer, "
            "feat_dom=description+features+domain model, "
            "dom=description+domain model."
        ),
    )
    parser.add_argument(
        "--sample", "-s",
        dest="samples",
        action="append",
        metavar="SAMPLE",
        help=(
            "Sample folder name(s) from data/ to include. May be repeated. "
            "Defaults to all samples discovered in data/."
        ),
    )
    parser.add_argument(
        "--repetitions", "-r",
        dest="repetitions",
        type=int,
        default=1,
        metavar="N",
        help="Number of times to repeat each (sample, tool, config) combination (default: 1).",
    )
    args = parser.parse_args()
    tools = args.tools if args.tools else ALL_TOOLS
    configs = args.configs if args.configs else ALL_CONFIGS
    samples = args.samples if args.samples else discover_samples()
    return args.mode, args.models, tools, configs, samples, args.repetitions


def main() -> None:
    mode, models, tools, configs, samples, repetitions = _parse_args()

    print(f"Samples: {samples}")

    # 1. Build all requests across every sample and repetition via the mode-specific builder.
    #    All are gathered first so each (api, model) gets a single batch.
    build = _BUILDERS[mode]
    all_requests: list[dict] = []
    for sample in samples:
        for rep in range(1, repetitions + 1):
            all_requests.extend(build(tools, configs, sample, rep=rep))

    total = len(all_requests) * len(models)
    print(f"Total requests per model: {len(all_requests)} "
          f"({len(samples)} sample(s) x {len(tools)} tool(s) x {len(configs)} config(s) x {repetitions} rep(s))")
    print(f"Total requests across all models: {total} ({len(all_requests)} x {len(models)} model(s))\n")

    answer = input(f"A total of {total} requests will be submitted. Proceed? [y/n] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        return

    # 2. Group models by API provider, then submit one batch per (api, model).
    by_api: dict[str, list[str]] = {}
    for model in models:
        api = api_for_model(model)
        by_api.setdefault(api, []).append(model)

    for api, api_models in by_api.items():
        submit_fn = PROVIDERS[api][0]
        client = make_client(api)

        for model in api_models:
            print(f"\n--- Submitting to {api} with model {model} "
                  f"({len(all_requests)} requests across {len(samples)} sample(s)) ---")

            batch_id = submit_fn(
                client,
                model=model,
                requests=all_requests,
            )
            save_batch_info(batch_id, model, api=api, mode=mode,
                            requests=all_requests)

    print("\nRun `python -m tools.generation_runner.check` to poll for results.")


if __name__ == "__main__":
    main()
