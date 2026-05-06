"""
tools/generation_runner/check.py

CLI entry point for polling batch results.  Reads the "mode" field from
each batch's JSON metadata and delegates to the mode-specific save_results()
for parsing and validation.

Usage:
    python -m tools.generation_runner.check
"""

import json
from pathlib import Path

from ._shared import BATCHES_DIR, PROVIDERS, make_client
from .controller.check import save_results as save_controller_results
from .test.check import save_results as save_test_results

_SAVE_RESULTS = {
    "controller": save_controller_results,
    "test": save_test_results,
}


def main() -> None:
    if not BATCHES_DIR.exists():
        print("No batches directory found. Nothing to check.")
        return

    batch_files = sorted(BATCHES_DIR.glob("*.json"))
    if not batch_files:
        print("No pending batches found.")
        return

    # Group by API so we only create one client per provider
    by_api: dict[str, list[tuple[Path, dict]]] = {}
    for batch_file in batch_files:
        info = json.loads(batch_file.read_text(encoding="utf-8"))
        api = info.get("api", "openai")
        by_api.setdefault(api, []).append((batch_file, info))

    for api, entries in by_api.items():
        if api not in PROVIDERS:
            for bf, _ in entries:
                print(f"Unknown API '{api}' in {bf.name}, skipping.")
            continue

        check_fn = PROVIDERS[api][1]
        client = make_client(api)

        for batch_file, info in entries:
            samples = sorted({r["sample"] for r in info["requests"]})
            sample_label = ", ".join(samples)
            mode = info["mode"]
            save_results = _SAVE_RESULTS[mode]
            print(f"[{sample_label}] ({mode}) batch {info['batch_id']}:")

            req_list = info["requests"]
            status, results_map = check_fn(client, info)

            if status == "pending":
                continue

            for req in req_list:
                custom_id = req["custom_id"]
                results_dir = Path(req["results_dir"])
                raw_text = results_map.get(custom_id) if results_map else None

                if status == "completed" and raw_text:
                    save_results(results_dir, raw_text)
                elif raw_text:
                    # Failed batch but we still got a response — save for audit
                    results_dir.mkdir(parents=True, exist_ok=True)
                    (results_dir / "raw_response.txt").write_text(raw_text, encoding="utf-8")
                    print(f"  Raw response saved to: {results_dir / 'raw_response.txt'}")

            batch_file.unlink()
            print(f"  Removed {batch_file.name}")


if __name__ == "__main__":
    main()
