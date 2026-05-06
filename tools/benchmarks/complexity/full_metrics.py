from pathlib import Path
from typing import Any

from radon.complexity import cc_rank, cc_visit
from radon.metrics import h_visit, mi_rank, mi_visit
from radon.raw import analyze

from .helper import extract_method_sources


def to_builtin(value: Any) -> Any:
    if hasattr(value, "_asdict"):
        return {key: to_builtin(item) for key, item in value._asdict().items()}
    if isinstance(value, dict):
        return {str(key): to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(item) for item in value]
    return value


def compute_cyclomatic_complexity_radon(code: str) -> int:
    blocks = cc_visit(code)
    return int(sum(block.complexity for block in blocks))


def compute_halstead_metrics(code: str) -> dict[str, Any]:
    halstead = h_visit(code)
    return to_builtin(halstead.total)


def build_sample_report(controller_path: Path, source: str) -> dict[str, Any]:
    cyclomatic_total = compute_cyclomatic_complexity_radon(source)
    raw_metrics = to_builtin(analyze(source))
    halstead_metrics = compute_halstead_metrics(source)
    maintainability_index = float(mi_visit(source, multi=True))

    return {
        "file_path": str(controller_path),
        "cyclomatic_complexity": {
            "total": cyclomatic_total,
            "rank": cc_rank(cyclomatic_total),
        },
        "raw_metrics": raw_metrics,
        "halstead_metrics": halstead_metrics,
        "maintainability_index": {
            "score": round(maintainability_index, 4),
            "rank": mi_rank(maintainability_index),
        },
    }


def build_method_reports(controller_path: Path, source: str) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for method_entry in extract_method_sources(source):
        method_source = method_entry["source"]

        cyclomatic_total = compute_cyclomatic_complexity_radon(method_source)
        raw_metrics = to_builtin(analyze(method_source))
        halstead_metrics = compute_halstead_metrics(method_source)
        maintainability_index = float(mi_visit(method_source, multi=True))

        reports.append(
            {
                "file_path": str(controller_path),
                "method": method_entry["method"],
                "cyclomatic_complexity": {
                    "total": cyclomatic_total,
                    "rank": cc_rank(cyclomatic_total),
                },
                "raw_metrics": raw_metrics,
                "halstead_metrics": halstead_metrics,
                "maintainability_index": {
                    "score": round(maintainability_index, 4),
                    "rank": mi_rank(maintainability_index),
                },
            }
        )

    return reports


def _is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _collect_numeric_paths(value: Any, path: tuple[str, ...], out: dict[tuple[str, ...], float]) -> None:
    if _is_numeric(value):
        out[path] = float(value)
        return

    if isinstance(value, dict):
        for key, item in value.items():
            _collect_numeric_paths(item, path + (str(key),), out)
        return

    if isinstance(value, list):
        for idx, item in enumerate(value):
            _collect_numeric_paths(item, path + (str(idx),), out)


def _get_numeric_values(report: dict[str, Any]) -> dict[tuple[str, ...], float]:
    out: dict[tuple[str, ...], float] = {}
    _collect_numeric_paths(report, tuple(), out)
    return out


def _smallest_non_zero_abs(values: list[float]) -> float:
    non_zero_abs = [abs(value) for value in values if value != 0]
    if not non_zero_abs:
        return 1.0
    return min(non_zero_abs)


def _normalize_by_path(value: Any, path: tuple[str, ...], denominators: dict[tuple[str, ...], float]) -> Any:
    if _is_numeric(value):
        denominator = denominators.get(path, 1.0)
        if denominator == 0:
            return value
        return round(float(value) / denominator, 4)

    if isinstance(value, dict):
        return {
            key: _normalize_by_path(item, path + (str(key),), denominators)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _normalize_by_path(item, path + (str(idx),), denominators)
            for idx, item in enumerate(value)
        ]

    return value


def normalize_reports(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not reports:
        return []

    per_report_values = [_get_numeric_values(report) for report in reports]
    all_paths = sorted({path for values in per_report_values for path in values})

    denominators: dict[tuple[str, ...], float] = {}
    for path in all_paths:
        samples = [values[path] for values in per_report_values if path in values]
        denominators[path] = _smallest_non_zero_abs(samples)

    return [_normalize_by_path(report, tuple(), denominators) for report in reports]


