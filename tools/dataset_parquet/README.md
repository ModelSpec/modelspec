# Dataset Parquet Tools

This folder contains tools to convert the ModelSpec dataset to and from Parquet format for Hugging Face upload.

## Requirements

Install dependencies before running:

```bash
pip install pandas pyarrow fastparquet
```

## Tools

### `code_to_dataset.py` — Build Parquet from source

Scans the `data/` folder and packages all samples into a single `.parquet` file.

```bash
# Run from the repo root
python tools/dataset_parquet/code_to_dataset.py
```

Output: `tools/dataset_parquet/modelspec_dataset.parquet`

---

### `dataset_to_code.py` — Restore source from Parquet

Reads a `.parquet` file and reconstructs the local folder structure under `data/`.
Also automatically writes `conftest.py` and `pytest.ini` to the output directory,
so pytest works out of the box without any manual setup.

```bash
# Run from the repo root (default: restores to data/)
python tools/dataset_parquet/dataset_to_code.py --parquet tools/dataset_parquet/modelspec_dataset.parquet

# Or specify custom paths
python tools/dataset_parquet/dataset_to_code.py --parquet path/to/file.parquet --output-dir path/to/output
```

## Round-trip

To verify the dataset round-trips correctly:

```bash
# Step 1: build parquet
python tools/dataset_parquet/code_to_dataset.py

# Step 2: restore to a test folder
# Note: dataset_to_code.py automatically writes conftest.py and pytest.ini
# to the output directory, so pytest works out of the box.
python tools/dataset_parquet/dataset_to_code.py --parquet tools/dataset_parquet/modelspec_dataset.parquet --output-dir data

# Step 3: run tests for a sample (from repo root)
# Note: test files are named testXxx.py, so specify them explicitly:

# PowerShell:
python -m pytest data
```
