"""
Shared helpers for tools/plots/complexity scripts.
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


def load_records(input_file: Path) -> list[dict]:
    """Return complexity records for controller eval with valid avg_cyclomatic_complexity."""
    records = []
    with open(input_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            agg = rec.get("aggregate") or {}
            if (
                rec.get("benchmark") == "complexity"
                and rec.get("eval_type") == "controller"
                and "error" not in rec
                and agg.get("avg_cyclomatic_complexity") is not None
            ):
                records.append(rec)
    return records


def compute_averages(
    records: list[dict],
    key_fn: Callable[[dict], str],
) -> dict[str, tuple[float, float]]:
    """
    Group records by key_fn, compute per-sample mean avg_cyclomatic_complexity,
    then average across samples so every sample is weighted equally.

    Returns {group_key: (mean, std)}.
    """
    cc: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for rec in records:
        key = key_fn(rec)
        cc[key][rec["sample"]].append(rec["aggregate"]["avg_cyclomatic_complexity"])

    averages: dict[str, tuple[float, float]] = {}
    for key, sample_map in cc.items():
        filtered = {s: vs for s, vs in sample_map.items() if s in SAMPLES}
        sample_means = [sum(vs) / len(vs) for vs in filtered.values()]
        sample_stds = [stdev(vs) for vs in filtered.values()]
        if sample_means:
            averages[key] = (
                sum(sample_means) / len(SAMPLES),
                sum(sample_stds) / len(SAMPLES),
            )
    return averages


def load_reference(ref_file: Path) -> dict[str, float]:
    """
    Read reference_complexity.jsonl produced by compute_reference.py.
    Returns {tool: avg_cc} averaged over SAMPLES.
    """
    cc_by_tool: dict[str, list[float]] = defaultdict(list)
    with open(ref_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("sample") not in SAMPLES:
                continue
            if rec.get("avg_cyclomatic_complexity") is None:
                continue
            cc_by_tool[rec["tool"]].append(rec["avg_cyclomatic_complexity"])
    return {
        tool: sum(vals) / len(SAMPLES)
        for tool, vals in cc_by_tool.items()
    }


def reference_overall(ref_by_tool: dict[str, float]) -> float:
    """Average per-tool reference values into a single float."""
    vals = list(ref_by_tool.values())
    return sum(vals) / len(vals)


def plot(
    averages: dict[str, tuple[float, float]],
    labels_map: dict[str, str],
    xlabel: str,
    output_file: Path,
    ylim: float = 12,
    ref_by_key: dict[str, float] | None = None,
) -> None:
    """
    Bar chart with error bars.  Known keys appear in labels_map order;
    any unexpected keys are appended sorted at the end.

    ref_by_key maps each group key to a reference avg_cyclomatic_complexity.
    When provided, a continuous axhline is drawn at the mean reference height.
    """
    ordered = [k for k in labels_map if k in averages]
    ordered += [k for k in sorted(averages) if k not in labels_map]

    labels = [labels_map.get(k, k) for k in ordered]
    values = [averages[k][0] for k in ordered]
    errors = [averages[k][1] for k in ordered]

    fig, ax = plt.subplots(figsize=(len(labels) * 1.5, 2.5))
    bars = ax.bar(labels, values, yerr=errors, capsize=5, error_kw={"elinewidth": 1.2})

    label_bbox = dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.85)

    if ref_by_key:
        ref_vals = [ref_by_key[k] for k in ordered if k in ref_by_key]
        ref_mean = sum(ref_vals) / len(ref_vals)
        color = bars[0].get_facecolor()
        ax.axhline(ref_mean, color=color, linewidth=2)
        ax.text(0.99, ref_mean, f"{ref_mean:.2f}",
                transform=ax.get_yaxis_transform(),
                ha="right", va="bottom", fontsize=9, color=color,
                bbox=label_bbox)

    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel("Cyclomatic Complexity", fontweight="bold")
    ax.set_ylim(0, ylim)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{val:.2f}", ha="center", va="bottom", fontsize=9,
                bbox=label_bbox)

    fig.tight_layout()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_file, dpi=150)
    print(f"Saved -> {output_file}")
