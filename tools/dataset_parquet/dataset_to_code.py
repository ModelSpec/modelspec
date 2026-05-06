import json
import argparse
import pandas as pd
from pathlib import Path


CONFTEST_CONTENT = """\
import pytest

from tools.middleware.factory import get_middleware_class


def pytest_addoption(parser):
    parser.addoption(
        "--modeling-tool",
        action="store",
        default="both",
        choices=["umple", "ecore", "both"],
    )


def pytest_generate_tests(metafunc):
    if "modelingTool" in metafunc.fixturenames:
        config_choice = metafunc.config.getoption("--modeling-tool")

        if config_choice == "both":
            modeling_tools = ["umple", "ecore"]
        else:
            modeling_tools = [config_choice]

        metafunc.parametrize("modelingTool", modeling_tools, ids=modeling_tools)


@pytest.fixture
def mw(modelingTool):
    return get_middleware_class(modelingTool)
"""

PYTEST_INI_CONTENT = """\
[pytest]
# configure pytest discovery to look in the local tests folder and pick up test*.py files
testpaths = tests
python_files = test*.py
"""


def write_file(path, content):
    """Write content to a file, creating directories if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Written: {path}")


def restore_single(base_path, json_str):
    if not json_str or not isinstance(json_str, str):
        return
    obj = json.loads(json_str)
    write_file(base_path / obj["path"], obj["code"])


def restore_list(base_path, json_str):
    if not json_str or not isinstance(json_str, str):
        return
    items = json.loads(json_str)
    for item in items:
        write_file(base_path / item["path"], item["code"])


def create_empty_file(path):
    """Create an empty file, creating directories if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    print(f"  Created: {path}")


def restore_sample(row, output_dir):
    """Restore one sample from a DataFrame row."""
    sample_name = row["sample_name"]
    sample_path = Path(output_dir) / sample_name
    print(f"\nRestoring {sample_name}...")

    # description
    if row.get("description"):
        write_file(sample_path / "description.txt", row["description"])

    # root __init__.py (empty)
    create_empty_file(sample_path / "__init__.py")

    # umple
    restore_single(sample_path, row.get("umple_model_ump"))
    restore_list(sample_path, row.get("umple_model_layer"))
    restore_list(sample_path, row.get("umple_controller"))

    # ecore
    restore_single(sample_path, row.get("ecore_model_emf"))
    restore_single(sample_path, row.get("ecore_model_ecore"))
    restore_list(sample_path, row.get("ecore_model_layer"))
    restore_list(sample_path, row.get("ecore_controller"))

    # features and tests
    restore_list(sample_path, row.get("features"))
    restore_list(sample_path, row.get("tests"))

    # tests/__init__.py (empty)
    create_empty_file(sample_path / "tests" / "__init__.py")


def write_pytest_files(output_dir):
    """Write conftest.py and pytest.ini to the output root directory."""
    output_dir = Path(output_dir)
    print("\nWriting pytest configuration files...")
    write_file(output_dir / "conftest.py", CONFTEST_CONTENT)
    write_file(output_dir / "pytest.ini", PYTEST_INI_CONTENT)


def main():
    parser = argparse.ArgumentParser(
        description="Restore dataset from a Parquet file into a local folder structure."
    )
    parser.add_argument(
        "--parquet",
        type=Path,
        default=Path("modelspec_dataset.parquet"),
        help="Path to the input .parquet file (default: modelspec_dataset.parquet)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="Directory to restore samples into (default: data/)"
    )
    args = parser.parse_args()

    print(f"Reading parquet from: {args.parquet}")
    df = pd.read_parquet(args.parquet)
    print(f"Found {len(df)} samples")

    for _, row in df.iterrows():
        restore_sample(row, args.output_dir)

    write_pytest_files(args.output_dir)

    print(f"\nDone! Restored to: {args.output_dir}")
    print("You can now run pytest directly!")


if __name__ == "__main__":
    main()