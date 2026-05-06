"""
Shared helpers for tools/plots/coverage scripts.
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
    """Return test eval records that have valid statement and branch coverage."""
    records = []
    with open(input_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            cov = rec.get("coverage") or {}
            if (
                rec.get("benchmark") == "test_pass_rate"
                and rec.get("eval_type") == "test"
                and "error" not in rec
                and cov.get("statement_coverage") is not None
                and cov.get("branch_coverage") is not None
            ):
                records.append(rec)
    return records


def compute_averages(
    records: list[dict],
    key_fn: Callable[[dict], str],
) -> dict[str, tuple[float, float, float, float]]:
    """
    Group records by key_fn and compute per-sample means, then average across
    samples so every sample is weighted equally.

    Returns {group_key: (stmt_mean, stmt_std, branch_mean, branch_std)}
    where all values are in [0, 1].
    """
    stmt: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    branch: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for rec in records:
        key = key_fn(rec)
        cov = rec["coverage"]
        stmt[key][rec["sample"]].append(cov["statement_coverage"])
        branch[key][rec["sample"]].append(cov["branch_coverage"])

    averages: dict[str, tuple[float, float, float, float]] = {}
    for key in stmt:
        s_map = {s: vs for s, vs in stmt[key].items() if s in SAMPLES}
        b_map = {s: vs for s, vs in branch[key].items() if s in SAMPLES}
        s_means = [sum(vs) / len(vs) for vs in s_map.values()]
        s_stds  = [stdev(vs) for vs in s_map.values()]
        b_means = [sum(vs) / len(vs) for vs in b_map.values()]
        b_stds  = [stdev(vs) for vs in b_map.values()]
        if s_means:
            averages[key] = (
                sum(s_means) / len(SAMPLES),
                sum(s_stds)  / len(SAMPLES),
                sum(b_means) / len(SAMPLES),
                sum(b_stds)  / len(SAMPLES),
            )
    return averages


def load_reference(ref_file: Path) -> dict[str, tuple[float, float]]:
    """
    Read reference_coverage.jsonl produced by compute_reference.py.
    Returns {tool: (stmt_mean, branch_mean)} averaged over SAMPLES.
    """
    stmt_by_tool: dict[str, list[float]] = defaultdict(list)
    branch_by_tool: dict[str, list[float]] = defaultdict(list)
    with open(ref_file, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("sample") not in SAMPLES:
                continue
            if rec.get("statement_coverage") is None or rec.get("branch_coverage") is None:
                continue
            stmt_by_tool[rec["tool"]].append(rec["statement_coverage"])
            branch_by_tool[rec["tool"]].append(rec["branch_coverage"])
    return {
        tool: (
            sum(stmt_by_tool[tool]) / len(SAMPLES),
            sum(branch_by_tool[tool]) / len(SAMPLES),
        )
        for tool in stmt_by_tool
    }


def reference_overall(ref_by_tool: dict[str, tuple[float, float]]) -> tuple[float, float]:
    """Average per-tool reference values into a single (stmt, branch) pair."""
    stmts    = [v[0] for v in ref_by_tool.values()]
    branches = [v[1] for v in ref_by_tool.values()]
    return (sum(stmts) / len(stmts), sum(branches) / len(branches))


def plot(
    averages: dict[str, tuple[float, float, float, float]],
    labels_map: dict[str, str],
    xlabel: str,
    output_file: Path,
    ylim: float = 100,
    ref_by_key: dict[str, tuple[float, float]] | None = None,
) -> None:
    """
    Grouped bar chart: statement and branch coverage side by side per group.
    Known keys appear in labels_map order; unexpected keys are appended sorted.

    ref_by_key maps each group key to a (stmt_ref, branch_ref) tuple in [0, 1].
    When provided, continuous axhlines are drawn at the mean reference heights.
    """
    ordered = [k for k in labels_map if k in averages]
    ordered += [k for k in sorted(averages) if k not in labels_map]

    labels = [labels_map.get(k, k) for k in ordered]
    s_vals = [averages[k][0] * 100 for k in ordered]
    s_errs = [averages[k][1] * 100 for k in ordered]
    b_vals = [averages[k][2] * 100 for k in ordered]
    b_errs = [averages[k][3] * 100 for k in ordered]

    x = list(range(len(labels)))
    width = 0.35

    fig, ax = plt.subplots(figsize=(len(labels) * 2.2, 2.5))
    bars_s = ax.bar(
        [i - width / 2 for i in x], s_vals, width,
        yerr=s_errs, capsize=4, error_kw={"elinewidth": 1.2},
    )
    bars_b = ax.bar(
        [i + width / 2 for i in x], b_vals, width,
        yerr=b_errs, capsize=4, error_kw={"elinewidth": 1.2},
    )

    label_bbox = dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.85)

    if ref_by_key:
        color_s = bars_s[0].get_facecolor()
        color_b = bars_b[0].get_facecolor()
        ref_vals = [ref_by_key[k] for k in ordered if k in ref_by_key]
        s_mean = sum(v[0] for v in ref_vals) / len(ref_vals)
        b_mean = sum(v[1] for v in ref_vals) / len(ref_vals)
        ax.axhline(s_mean * 100, color=color_s, linewidth=2)
        ax.axhline(b_mean * 100, color=color_b, linewidth=2)
        trans = ax.get_yaxis_transform()
        ax.text(0.99, s_mean * 100, f"{s_mean * 100:.1f}%",
                transform=trans, ha="right", va="bottom",
                fontsize=8, color=color_s, bbox=label_bbox)
        ax.text(0.99, b_mean * 100, f"{b_mean * 100:.1f}%",
                transform=trans, ha="right", va="top",
                fontsize=8, color=color_b, bbox=label_bbox)

    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel("Coverage (%)", fontweight="bold")
    ax.set_ylim(0, ylim)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    for bar, val in zip(bars_s, s_vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=8,
                bbox=label_bbox)
    for bar, val in zip(bars_b, b_vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=8,
                bbox=label_bbox)

    fig.tight_layout()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_file, dpi=150)
    print(f"Saved -> {output_file}")
