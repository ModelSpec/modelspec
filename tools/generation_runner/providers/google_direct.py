"""Google GenAI direct API provider for Gemma models (no batch API support)."""

import json
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from google import genai

from .misc import SYSTEM_PROMPT

_BATCHES_DIR = Path(__file__).resolve().parents[1] / "batches"


def _call_one(model: str, req: dict) -> tuple[str, str | None]:
    """Worker: creates its own client (clients are not picklable across processes)."""
    from google import genai
    from google.genai import types

    custom_id = req["custom_id"]
    client = genai.Client()
    while True:
        try:
            response = client.models.generate_content(
                model=model,
                contents=req["prompt"],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            return custom_id, response.text
        except Exception as exc:
            if "429" in str(exc):
                print(f"  [{custom_id}] rate-limited (429), retrying in 30s...", flush=True)
                time.sleep(30)
            else:
                print(f"  [{custom_id}] error: {exc}", flush=True)
                return custom_id, None


def submit(client: genai.Client, *, model: str, requests: list[dict]) -> str:
    """Submit all requests in parallel. Appends each result to a JSONL sidecar as it arrives."""
    batch_id = f"direct-{uuid.uuid4().hex[:12]}"
    _BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    sidecar = _BATCHES_DIR / f"{batch_id}_results.jsonl"

    with ProcessPoolExecutor() as pool, sidecar.open("a", encoding="utf-8") as f:
        futures = {pool.submit(_call_one, model, req): req["custom_id"] for req in requests}
        for future in as_completed(futures):
            custom_id, text = future.result()
            print(f"  [{custom_id}] {'ok' if text is not None else 'error'}", flush=True)
            f.write(json.dumps({"custom_id": custom_id, "text": text}) + "\n")
            f.flush()

    print(f"Direct batch complete: {batch_id}  ({len(requests)} requests)")
    return batch_id


def check(client: genai.Client, info: dict) -> tuple[str, dict[str, str] | None]:
    """Read pre-computed results. Always returns immediately (no polling needed).

    Returns a 2-tuple:
      - status: one of "pending", "completed", "failed"
      - results_map: dict mapping custom_id -> raw response text, or None if failed
    """
    batch_id = info["batch_id"]
    sidecar = _BATCHES_DIR / f"{batch_id}_results.jsonl"

    if not sidecar.exists():
        print(f"  Results file not found: {sidecar}")
        return "failed", None

    results_map: dict[str, str] = {}
    any_failed = False
    with sidecar.open(encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if entry["text"] is not None:
                results_map[entry["custom_id"]] = entry["text"]
            else:
                any_failed = True
    sidecar.unlink()

    if not results_map and any_failed:
        return "failed", None

    return "failed" if any_failed else "completed", results_map
