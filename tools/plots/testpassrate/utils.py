"""
Shared helpers for tools/plots/testpassrate scripts.
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from ..utils import (  # noqa: F401  (re-exported for scripts to import from here)
    CONFIG_GROUP_LABELS,
    MODEL_LABELS,
    SAMPLES,
    TOOL_LABELS,
    config_group,
    stdev,
)


def load_records(input_file: Path, eval_type: str) -> list[dict]:
    """Return all valid test_pass_rate records for the given eval_type."""
    records = []
    with open(input_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if (
                rec.get("benchmark") == "test_pass_rate"
                and rec.get("eval_type") == eval_type
                and "error" not in rec
                and rec.get("pass_rate") is not None
            ):
                records.append(rec)
    return records


def compute_averages(
    records: list[dict],
    key_fn: Callable[[dict], str],
) -> dict[str, tuple[float, float]]:
    """
    Group records by key_fn, then compute per-sample mean pass_rate and average
    across samples so every sample is weighted equally.

    Returns {group_key: (mean, std)} where values are in [0, 1].
    """
    rates: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for rec in records:
        rates[key_fn(rec)][rec["sample"]].append(rec["pass_rate"])

    averages: dict[str, tuple[float, float]] = {}
    for key, sample_map in rates.items():
        filtered = {s: vs for s, vs in sample_map.items() if s in SAMPLES}
        sample_means = [sum(vs) / len(vs) for vs in filtered.values()]
        sample_stds = [stdev(vs) for vs in filtered.values()]
        if sample_means:
            averages[key] = (
                sum(sample_means) / len(SAMPLES),
                sum(sample_stds) / len(SAMPLES),
            )
    return averages


def plot(
    averages: dict[str, tuple[float, float]],
    labels_map: dict[str, str],
    xlabel: str,
    output_file: Path,
    ylim: float = 85,
) -> None:
    """
    Bar chart with error bars.  Known keys appear in labels_map order;
    any unexpected keys are appended sorted at the end.
    """
    ordered = [k for k in labels_map if k in averages]
    ordered += [k for k in sorted(averages) if k not in labels_map]

    labels = [labels_map.get(k, k) for k in ordered]
    values = [averages[k][0] * 100 for k in ordered]
    errors = [averages[k][1] * 100 for k in ordered]

    fig, ax = plt.subplots(figsize=(len(labels) * 1.5, 2.5))
    bars = ax.bar(labels, values, yerr=errors, capsize=5, error_kw={"elinewidth": 1.2})

    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel("Test Pass Rate (%)", fontweight="bold")
    ax.set_ylim(0, ylim)

    label_bbox = dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.85)
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{val:.1f}%",
            ha="center", va="bottom", fontsize=9,
            bbox=label_bbox,
        )

    fig.tight_layout()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_file, dpi=150)
    print(f"Saved -> {output_file}")
