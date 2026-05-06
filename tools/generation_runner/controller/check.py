"""Controller generation: result parsing and file saving."""

import re
from pathlib import Path

_FILE_TAG = re.compile(r'<file name="([^"]+)">\n?(.*?)\n?</file>', re.DOTALL)


def save_results(results_dir: Path, raw_text: str) -> bool:
    """Parse the LLM response, save each file. Returns True on success.

    Controller mode requires that the response contains at least a
    ``controller.py`` file.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "raw_response.txt").write_text(raw_text, encoding="utf-8")
    print(f"  Raw response saved to: {results_dir / 'raw_response.txt'}")

    files = dict(_FILE_TAG.findall(raw_text))
    if "controller.py" not in files:
        print("  Parse error: Missing required controller.py in response")
        return False

    for filename, content in files.items():
        out_path = results_dir / filename
        out_path.write_text(content, encoding="utf-8")
        print(f"  Saved: {out_path}")
    return True
