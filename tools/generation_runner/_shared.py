"""
Shared constants, dataclasses, and helpers used by both controller and test
generation modes.
"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .utils import stub_source, stub_model_source, sanitize_model_name
from .providers import *

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_MODELS = ["gpt-5.4", "gpt-5.4-nano", "claude-opus-4-7", "gemma-4-31b-it"]
# Cheap models for testing the pipeline.
# DEFAULT_MODELS = ["gpt-5.4-nano", "claude-haiku-4-5-20251001", "gemma-4-31b-it"]
ALL_TOOLS = ["umple", "ecore"]
ALL_CONFIGS = ["feat_gen", "gen"]
ALL_MODES = ["controller", "test"]

ROOT = Path(__file__).resolve().parents[2]  # modelspec/
DATA_DIR = ROOT / "data"
BATCHES_DIR = ROOT / "tools" / "generation_runner" / "batches"
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def discover_samples() -> list[str]:
    """Return all sample folder names in data/ (excluding hidden/private dirs)."""
    return sorted(
        p.name for p in DATA_DIR.iterdir()
        if p.is_dir() and not p.name.startswith((".", "_"))
    )


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass
class Config:
    name: str
    has_features: bool
    model_type: str  # "gen" | "dom"
    prompt_template: str


def load_configs(mode: str) -> dict[str, Config]:
    def _tpl(name: str) -> str:
        return (PROMPTS_DIR / mode / f"prompt_{name}.txt").read_text(encoding="utf-8")

    return {
        "feat_gen": Config("feat_gen", True,  "gen", _tpl("feat_gen")),
        "gen":      Config("gen",      False, "gen", _tpl("gen")),
        "feat_dom": Config("feat_dom", True,  "dom", _tpl("feat_dom")),
        "dom":      Config("dom",      False, "dom", _tpl("dom")),
    }


# ---------------------------------------------------------------------------
# File reading helpers
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_features(features_dir: Path) -> str:
    """Concatenate all .feature files into a single string."""
    parts = []
    for feat in sorted(features_dir.glob("*.feature")):
        parts.append(f"<file name=\"{feat.name}\">\n{read_text(feat)}\n</file>")
    return "\n\n".join(parts)


def stub_controller(controller_path: Path) -> str:
    """Return the stubbed version of the controller source."""
    return stub_source(read_text(controller_path))


def collect_model_layer(tool_dir: Path) -> str:
    """Concatenate all generated model-layer .py files (excluding __init__.py)."""
    layer_dir = tool_dir / "generated_model_layer"
    parts = []
    for py_file in sorted(layer_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        parts.append(f"<file name=\"{py_file.name}\">\n{stub_model_source(read_text(py_file))}\n</file>")
    return "\n\n".join(parts)


def read_domain_model(tool_dir: Path, tool: str) -> str:
    """Return the domain model source wrapped in an XML file tag."""
    ext = "ump" if tool == "umple" else "emf"
    content = read_text(tool_dir / "model" / f"model.{ext}")
    return f"<file name=\"model.{ext}\">\n{content}\n</file>"


def build_prompt(config: Config, stubbed_controller: str, description: str,
                 features: str, model_context: str, **extra) -> str:
    kwargs: dict = {
        "description": description,
        "stubbed_controller": stubbed_controller,
        "model_context": model_context,
        **extra,
    }
    if config.has_features:
        kwargs["features"] = features
    return config.prompt_template.format(**kwargs)


def results_dir(mode: str, model: str, batch_id: str, tool: str, config: str, sample: str, rep: int) -> Path:
    return ROOT / "results" / sample / tool / sanitize_model_name(model) / mode / config / batch_id / f"r{rep}"


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

def make_client(api: str):
    """Lazily create the appropriate API client."""
    if api == "openai":
        from openai import OpenAI
        return OpenAI()
    elif api in ("google", "google_direct"):
        from google import genai
        return genai.Client()
    elif api == "openrouter_direct":
        import os
        from openrouter import OpenRouter
        return OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY", ""))
    else:
        import anthropic
        return anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Batch metadata
# ---------------------------------------------------------------------------

def save_batch_info(batch_id: str, model: str, api: str, mode: str,
                    requests: list[dict]) -> None:
    """Save batch metadata to a JSON file in the batches directory.

    Also writes system_prompt.txt and user_prompt.txt into each request's
    results directory for audit purposes.
    """
    BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    request_entries = []
    for r in requests:
        rdir = results_dir(mode, model, batch_id, r["tool"], r["config"], r["sample"], r["rep"])
        rdir.mkdir(parents=True, exist_ok=True)
        (rdir / "system_prompt.txt").write_text(SYSTEM_PROMPT, encoding="utf-8")
        (rdir / "user_prompt.txt").write_text(r["prompt"], encoding="utf-8")
        request_entries.append({
            "custom_id": r["custom_id"],
            "sample": r["sample"],
            "tool": r["tool"],
            "config": r["config"],
            "rep": r["rep"],
            "results_dir": str(rdir),
        })

    batch_info = {
        "batch_id": batch_id,
        "api": api,
        "mode": mode,
        "model": model,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "requests": request_entries,
    }
    batch_file = BATCHES_DIR / f"{batch_id}.json"
    batch_file.write_text(json.dumps(batch_info, indent=2), encoding="utf-8")
    print(f"Batch info saved to: {batch_file}")
