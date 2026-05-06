"""Google GenAI Batch API provider (Gemini / Gemma models)."""

from google import genai

from .misc import SYSTEM_PROMPT


def submit(client: genai.Client, *, model: str, requests: list[dict]) -> str:
    """Submit a batch request. Returns the batch job name.

    Each entry in *requests* must have:
        custom_id (str): unique identifier for the request
        prompt    (str): the user message to send
    """
    inline_requests = [
        {
            "contents": [
                {
                    "parts": [{"text": req["prompt"]}],
                    "role": "user",
                }
            ],
            "config": {
                "system_instruction": {
                    "parts": [{"text": SYSTEM_PROMPT}],
                },
            },
        }
        for req in requests
    ]

    batch_job = client.batches.create(
        model=model,
        src=inline_requests,
        config={
            "display_name": f"{requests[0]['custom_id']}-batch",
        },
    )
    print(f"Created batch job: {batch_job.name}  (state: {batch_job.state.name})")
    return batch_job.name


def check(client: genai.Client, info: dict) -> tuple[str, dict[str, str] | None]:
    """Check batch status and return (status, results_map).

    Returns a 2-tuple:
      - status: one of "pending", "completed", "failed"
      - results_map: dict mapping custom_id -> raw response text, or None if pending
    """
    batch_job = client.batches.get(name=info["batch_id"])
    print(f"  google status: {batch_job.state.name}")

    terminal_states = {
        "JOB_STATE_SUCCEEDED",
        "JOB_STATE_FAILED",
        "JOB_STATE_CANCELLED",
        "JOB_STATE_EXPIRED",
    }
    if batch_job.state.name not in terminal_states:
        return "pending", None

    if batch_job.state.name != "JOB_STATE_SUCCEEDED":
        if batch_job.error:
            print(f"    error: {batch_job.error}")
        return "failed", None

    # Retrieve inline responses
    req_list = info["requests"]
    results_map: dict[str, str] = {}
    any_failed = False

    if batch_job.dest and batch_job.dest.inlined_responses:
        for i, inline_response in enumerate(batch_job.dest.inlined_responses):
            custom_id = req_list[i]["custom_id"] if i < len(req_list) else f"unknown-{i}"
            if inline_response.response:
                results_map[custom_id] = inline_response.response.text
            else:
                print(f"  Request {custom_id} returned an error: {inline_response.error}")
                any_failed = True

    if not results_map and any_failed:
        return "failed", None

    status = "failed" if any_failed else "completed"
    return status, results_map
