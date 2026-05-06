"""Anthropic Message Batches API provider."""

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

from .misc import SYSTEM_PROMPT


def submit(client: anthropic.Anthropic, *, model: str, requests: list[dict]) -> str:
    """Submit a batch request. Returns the batch ID.

    Each entry in *requests* must have:
        custom_id (str): unique identifier for the request
        prompt    (str): the user message to send
    """
    batch_requests = [
        Request(
            custom_id=req["custom_id"],
            params=MessageCreateParamsNonStreaming(
                model=model,
                max_tokens=32000,
                messages=[
                    {"role": "user", "content": req["prompt"]},
                ],
                system=SYSTEM_PROMPT,
            ),
        )
        for req in requests
    ]
    message_batch = client.messages.batches.create(requests=batch_requests)
    print(f"Created batch: {message_batch.id}  (status: {message_batch.processing_status})")
    return message_batch.id


def check(client: anthropic.Anthropic, info: dict) -> tuple[str, dict[str, str] | None]:
    """Check batch status and return (status, results_map).

    Returns a 2-tuple:
      - status: one of "pending", "completed", "failed"
      - results_map: dict mapping custom_id -> raw response text, or None if pending
    """
    batch = client.messages.batches.retrieve(info["batch_id"])
    print(f"  anthropic status: {batch.processing_status}")

    if batch.processing_status != "ended":
        return "pending", None

    results_map: dict[str, str] = {}
    any_failed = False
    for result in client.messages.batches.results(info["batch_id"]):
        if result.result.type == "succeeded":
            results_map[result.custom_id] = result.result.message.content[0].text
        else:
            print(f"  Request {result.custom_id} ended with result type: {result.result.type}")
            if result.result.type == "errored":
                print(f"    error: {result.result.error}")
            any_failed = True

    if not results_map and any_failed:
        return "failed", None

    status = "failed" if any_failed else "completed"
    return status, results_map
