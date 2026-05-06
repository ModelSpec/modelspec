"""
Shared helpers for tools/plots/size scripts.
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
    """Return complexity records for controller eval with valid LOC and chars fields."""
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
                and agg.get("total_lines_of_code") is not None
                and agg.get("total_characters_of_code") is not None
            ):
                records.append(rec)
    return records


def compute_averages(
    records: list[dict],
    key_fn: Callable[[dict], str],
) -> dict[str, tuple[float, float, float, float]]:
    """
    Group records by key_fn, compute per-sample means for LOC and chars,
    then average across samples so every sample is weighted equally.

    Returns {group_key: (loc_mean, loc_std, chars_mean, chars_std)}.
    """
    loc: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    chars: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for rec in records:
        key = key_fn(rec)
        agg = rec["aggregate"]
        loc[key][rec["sample"]].append(agg["total_lines_of_code"])
        chars[key][rec["sample"]].append(agg["total_characters_of_code"])

    averages: dict[str, tuple[float, float, float, float]] = {}
    for key in loc:
        l_map = {s: vs for s, vs in loc[key].items() if s in SAMPLES}
        c_map = {s: vs for s, vs in chars[key].items() if s in SAMPLES}
        l_means = [sum(vs) / len(vs) for vs in l_map.values()]
        l_stds  = [stdev(vs) for vs in l_map.values()]
        c_means = [sum(vs) / len(vs) for vs in c_map.values()]
        c_stds  = [stdev(vs) for vs in c_map.values()]
        if l_means:
            averages[key] = (
                sum(l_means) / len(SAMPLES),
                sum(l_stds)  / len(SAMPLES),
                sum(c_means) / len(SAMPLES),
                sum(c_stds)  / len(SAMPLES),
            )
    return averages


def load_reference(ref_file: Path) -> dict[str, tuple[float, float]]:
    """
    Read reference_size.jsonl produced by compute_reference.py.
    Returns {tool: (loc_mean, chars_mean)} averaged over SAMPLES.
    """
    loc_by_tool: dict[str, list[float]] = defaultdict(list)
    chars_by_tool: dict[str, list[float]] = defaultdict(list)
    with open(ref_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("sample") not in SAMPLES:
                continue
            if rec.get("lines_of_code") is None or rec.get("characters_of_code") is None:
                continue
            loc_by_tool[rec["tool"]].append(rec["lines_of_code"])
            chars_by_tool[rec["tool"]].append(rec["characters_of_code"])
    return {
        tool: (
            sum(loc_by_tool[tool]) / len(SAMPLES),
            sum(chars_by_tool[tool]) / len(SAMPLES),
        )
        for tool in loc_by_tool
    }


def reference_overall(ref_by_tool: dict[str, tuple[float, float]]) -> tuple[float, float]:
    """Average per-tool reference values into a single (loc, chars) pair."""
    locs  = [v[0] for v in ref_by_tool.values()]
    chars = [v[1] for v in ref_by_tool.values()]
    return (sum(locs) / len(locs), sum(chars) / len(chars))


def plot(
    averages: dict[str, tuple[float, float, float, float]],
    labels_map: dict[str, str],
    xlabel: str,
    ylabel: str,
    output_file: Path,
    metric: str,
    ref_by_key: dict[str, tuple[float, float]] | None = None,
) -> None:
    """
    Bar chart with error bars for one code-size metric.
    metric must be "loc" or "chars"; selects the appropriate pair from averages.
    Known keys appear in labels_map order; unexpected keys are appended sorted.

    ref_by_key maps each group key to a (loc_ref, chars_ref) tuple.
    When provided, a continuous axhline is drawn at the mean reference height.
    """
    val_idx, err_idx, ref_idx = (0, 1, 0) if metric == "loc" else (2, 3, 1)

    ordered = [k for k in labels_map if k in averages]
    ordered += [k for k in sorted(averages) if k not in labels_map]

    labels = [labels_map.get(k, k) for k in ordered]
    values = [averages[k][val_idx] for k in ordered]
    errors = [averages[k][err_idx] for k in ordered]

    fig, ax = plt.subplots(figsize=(len(labels) * 1.5, 2.5))
    bars = ax.bar(labels, values, yerr=errors, capsize=5, error_kw={"elinewidth": 1.2})

    label_bbox = dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.85)

    if ref_by_key:
        ref_vals = [ref_by_key[k] for k in ordered if k in ref_by_key]
        ref_mean = sum(v[ref_idx] for v in ref_vals) / len(ref_vals)
        color = bars[0].get_facecolor()
        ax.axhline(ref_mean, color=color, linewidth=2)
        ax.text(0.99, ref_mean, f"{ref_mean:.0f}",
                transform=ax.get_yaxis_transform(),
                ha="right", va="bottom", fontsize=9, color=color,
                bbox=label_bbox)

    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.0f}", ha="center", va="bottom", fontsize=9,
                bbox=label_bbox)

    fig.tight_layout()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_file, dpi=150)
    print(f"Saved -> {output_file}")
