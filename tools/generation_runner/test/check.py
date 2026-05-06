"""Test generation: result parsing and file saving."""

import re
from pathlib import Path

_FILE_TAG = re.compile(r'<file name="([^"]+)">\n?(.*?)\n?</file>', re.DOTALL)


def save_results(results_dir: Path, raw_text: str) -> bool:
    """Parse the LLM response, save each file. Returns True on success.

    Test mode accepts any number of Python test files — no specific
    filename is required, but at least one ``<file>`` tag must be present.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "raw_response.txt").write_text(raw_text, encoding="utf-8")
    print(f"  Raw response saved to: {results_dir / 'raw_response.txt'}")

    files = dict(_FILE_TAG.findall(raw_text))
    if not files:
        print("  Parse error: No <file> tags found in response")
        return False

    for filename, content in files.items():
        out_path = results_dir / filename
        out_path.write_text(content, encoding="utf-8")
        print(f"  Saved: {out_path}")
    return True
