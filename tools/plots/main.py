#!/usr/bin/env python3
"""
Run every plotting script in tools/plots/ to regenerate all figures.

Usage
-----
    python -m tools.plots.main [--input FILE]
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLOT_MODULES = [
    # Test pass rate — controller generation
    "tools.plots.testpassrate.controller.config_pass_rate",
    "tools.plots.testpassrate.controller.model_pass_rate",
    "tools.plots.testpassrate.controller.tool_pass_rate",
    # Test pass rate — test generation
    "tools.plots.testpassrate.test.config_pass_rate",
    "tools.plots.testpassrate.test.model_pass_rate",
    "tools.plots.testpassrate.test.tool_pass_rate",
    # Coverage
    "tools.plots.coverage.config_coverage",
    "tools.plots.coverage.model_coverage",
    "tools.plots.coverage.tool_coverage",
    # Cyclomatic complexity
    "tools.plots.complexity.config_complexity",
    "tools.plots.complexity.model_complexity",
    "tools.plots.complexity.tool_complexity",
    # Code size — lines of code
    "tools.plots.size.loc.config_loc",
    "tools.plots.size.loc.model_loc",
    "tools.plots.size.loc.tool_loc",
    # Code size — characters of code
    "tools.plots.size.coc.config_coc",
    "tools.plots.size.coc.model_coc",
    "tools.plots.size.coc.tool_coc",
]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=None,
        metavar="FILE",
        help="Path to pipeline_results.jsonl (overrides each script's default)",
    )
    args = parser.parse_args(argv)

    failed = []
    for module in PLOT_MODULES:
        cmd = [sys.executable, "-m", module]
        if args.input:
            cmd += ["--input", args.input]
        print(f"\n--- {module} ---")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            failed.append(module)

    print()
    if failed:
        print(f"Failed ({len(failed)}/{len(PLOT_MODULES)}):")
        for m in failed:
            print(f"  {m}")
        return 1

    print(f"All {len(PLOT_MODULES)} plots updated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
