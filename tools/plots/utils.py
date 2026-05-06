"""
Shared constants and pure helpers for all tools/plots subpackages.
No I/O, no matplotlib — safe to import anywhere without side-effects.
"""

import math

SAMPLES = [
    "AssetPlus",
    "BikeTourPlus",
    "BusTransportationManagementSystem",
    "CheECSEManager",
    "Facepage",
    "HomeForTheElderly",
    "House",
    "LocalLoop",
    "MeetingGroups",
    "Symboleo",
]

MODEL_LABELS: dict[str, str] = {
    "claude_opus_4_7": "Claude Opus 4.7",
    "gpt_5_4":         "GPT-5.4",
    "gpt_5_4_nano":    "GPT-5.4 Nano",
    "gemma_4_31b_it":  "Gemma 4 31B",
}

TOOL_LABELS: dict[str, str] = {
    "ecore": "Ecore",
    "umple": "Umple",
}

CONFIG_GROUP_LABELS: dict[str, str] = {
    "with_features":    "with\nGherkin",
    "without_features": "without\nGherkin",
}


def config_group(config: str) -> str:
    return "with_features" if config.startswith("feat_") else "without_features"


def stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))
