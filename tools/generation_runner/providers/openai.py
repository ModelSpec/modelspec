"""OpenAI Batch API provider."""

import io
import json
from pathlib import Path

from openai import OpenAI

from .misc import SYSTEM_PROMPT


def submit(client: OpenAI, *, model: str, requests: list[dict]) -> str:
    """Submit a batch request. Returns the batch ID.

    Each entry in *requests* must have:
        custom_id (str): unique identifier for the request
        prompt    (str): the user message to send
    """
    jsonl_lines = "\n".join(
        json.dumps({
            "custom_id": req["custom_id"],
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": req["prompt"]},
                ],
            },
        })
        for req in requests
    )

    batch_input_file = client.files.create(
        file=("batch_input.jsonl", io.BytesIO(jsonl_lines.encode("utf-8"))),
        purpose="batch",
    )
    print(f"Uploaded batch input file: {batch_input_file.id}")

    batch = client.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": f"{model} generation batch"},
    )
    print(f"Created batch: {batch.id}  (status: {batch.status})")
    return batch.id


def check(client: OpenAI, info: dict) -> tuple[str, dict[str, str] | None]:
    """Check batch status and return (status, results_map).

    Returns a 2-tuple:
      - status: one of "pending", "completed", "failed"
      - results_map: dict mapping custom_id -> raw response text, or None if pending
    """
    batch = client.batches.retrieve(info["batch_id"])
    print(f"  openai status: {batch.status}")

    terminal_statuses = {"completed", "failed", "expired", "cancelled"}
    if batch.status not in terminal_statuses:
        return "pending", None

    if batch.status != "completed":
        if batch.errors and batch.errors.data:
            for err in batch.errors.data:
                print(f"    error: {err.message}")
        return "failed", None

    if not batch.output_file_id:
        print("  Batch completed but no output file was produced.")
        return "failed", None

    output_content = client.files.content(batch.output_file_id).text
    results_map: dict[str, str] = {}
    for line in output_content.strip().splitlines():
        entry = json.loads(line)
        custom_id = entry["custom_id"]
        results_map[custom_id] = entry["response"]["body"]["choices"][0]["message"]["content"]

    return "completed", results_map
