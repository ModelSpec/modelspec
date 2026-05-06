# Benchmarks

This directory contains quality-measurement benchmarks for generated controllers and test suites. Results are written as **JSONL** (one JSON object per line), making them easy to append to and reload for downstream analysis (e.g. plotting).

## Benchmarks

### `complexity` — Cyclomatic complexity & maintainability index

Measures all `.py` files inside a single controller directory using [Radon](https://radon.readthedocs.io/).

```bash
# Core metrics (cyclomatic complexity + maintainability index), per method
python -m tools.benchmarks.complexity.benchmark \
    --controller results/AssetPlus/ecore/claude_opus_4_7/controller/feat_gen/<batch>/r1

# Full metrics (adds raw LOC and Halstead), aggregated per file instead of per method
python -m tools.benchmarks.complexity.benchmark \
    --controller data/AssetPlus/ecore/controller \
    --metric full \
    --granularity sample

# Custom output path
python -m tools.benchmarks.complexity.benchmark \
    --controller results/AssetPlus/ecore/claude_opus_4_7/controller/feat_gen/<batch>/r1 \
    --output-dir /tmp \
    --output-name complexity_results.jsonl
```

#### Arguments

| Argument             | Default      | Description                                                                            |
| -------------------- | ------------ | -------------------------------------------------------------------------------------- |
| `--controller DIR`   | _(required)_ | Directory containing the `.py` files to measure (`__init__.py` excluded)               |
| `--metric`           | `core`       | `core` = complexity + maintainability; `full` = adds raw LOC and Halstead              |
| `--granularity`      | `method`     | `method` = one record per method; `sample` = one record per file                       |
| `--output-dir DIR`   | this folder  | Directory for the JSONL output file                                                    |
| `--output-name FILE` | auto         | JSONL filename (default: `controller_complexity_results_<metric>_<granularity>.jsonl`) |

---

### `testpassrate` — Test pass rate & statement/branch coverage

Sets up a temporary Python package that mirrors the `data/` layout so that all relative imports resolve correctly, then runs pytest with JUnit XML and JSON coverage reports.

Supports two evaluation directions:

- **Controller eval** — ground-truth test suite vs. a generated `controller.py`
- **Test eval** — a generated test suite vs. the ground-truth `controller.py`

```bash
# Evaluate a generated controller against the ground-truth tests
python -m tools.benchmarks.testpassrate.benchmark \
    --controller results/AssetPlus/ecore/claude_opus_4_7/controller/feat_gen/<batch>/r1 \
    --tests data/AssetPlus/tests \
    --output tools/benchmarks/testpassrate/results.jsonl

# Evaluate a generated test suite against the ground-truth controller
python -m tools.benchmarks.testpassrate.benchmark \
    --controller data/AssetPlus/ecore/controller \
    --tests results/AssetPlus/ecore/claude_opus_4_7/test/feat_gen/<batch>/r1 \
    --output tools/benchmarks/testpassrate/results.jsonl
```

#### Arguments

| Argument              | Default      | Description                                                       |
| --------------------- | ------------ | ----------------------------------------------------------------- |
| `--controller DIR`    | _(required)_ | Folder containing `controller.py` to evaluate                     |
| `--tests DIR`         | _(required)_ | Folder containing the test files to run                           |
| `--output FILE.jsonl` | stdout       | Append result as a JSONL line; prints JSON to stdout if omitted   |
| `--data-root DIR`     | `repo/data`  | Path to the `data/` directory (for model layer and conftest)      |
| `--sample NAME`       | inferred     | Sample name, e.g. `AssetPlus` (inferred from path if omitted)     |
| `--tool`              | inferred     | Modeling tool: `ecore` or `umple` (inferred from path if omitted) |

**Output record fields**

```jsonc
{
  "timestamp": "2026-04-30T13:17:18Z",
  "controller_path": ".../r1",
  "test_path": ".../tests",
  "sample": "AssetPlus",
  "tool": "ecore",
  "model": "claude_opus_4_7", // null when using a data/ path
  "eval_type": "controller", // null when using a data/ path
  "config": "feat_gen",
  "batch_id": "msgbatch_...",
  "repetition": "r1",
  "pass_count": 57,
  "fail_count": 84,
  "error_count": 0,
  "skip_count": 0,
  "total_count": 141,
  "pass_rate": 0.4043,
  "test_cases": [
    // one entry per test
    {
      "name": "...::testAddAssetSuccess[ecore-...]",
      "result": "passed",
      "duration_s": 0.03,
    },
    {
      "name": "...::testAddAssetSuccess[ecore-...]",
      "result": "failed",
      "duration_s": 0.002,
      "message": "...",
    },
  ],
  "coverage": {
    "statement_coverage": 0.9574,
    "covered_lines": 289,
    "num_statements": 303,
    "branch_coverage": 0.9632,
    "covered_branches": 183,
    "num_branches": 190,
  },
  "pytest_returncode": 1,
}
```

Coverage requires `pytest-cov` (included in `requirements-dev.txt`). If not installed, the `coverage` field is omitted.

---

### `main` — Full evaluation pipeline

Scans the entire `results/` tree and runs all applicable benchmarks in parallel, appending results to a JSONL file as each entry completes. Partial results are preserved if the run is interrupted.

| Eval type  | Benchmarks run                   |
| ---------- | -------------------------------- |
| controller | `test_pass_rate` + `complexity`  |
| test       | `test_pass_rate` (with coverage) |

```bash
# Evaluate everything
python -m tools.benchmarks.main

# Restrict by eval type, sample, or model (all repeatable / combinable)
python -m tools.benchmarks.main --mode controller
python -m tools.benchmarks.main --sample AssetPlus --sample BikeTourPlus
python -m tools.benchmarks.main --model claude_opus_4_7

# Custom output path and worker count
python -m tools.benchmarks.main \
    --output my_results.jsonl \
    --workers 8
```

#### Arguments

| Argument              | Default                       | Description                                      |
| --------------------- | ----------------------------- | ------------------------------------------------ |
| `--results-dir DIR`   | `repo/results`                | Root results directory to scan                   |
| `--data-dir DIR`      | `repo/data`                   | Ground-truth data directory                      |
| `--output FILE.jsonl` | `repo/pipeline_results.jsonl` | Output JSONL file (appended to, not overwritten) |
| `--workers N`         | `cpu_count`                   | Number of parallel worker processes              |
| `--mode`              | both                          | Restrict to `controller` or `test` eval type     |
| `--sample NAME`       | all                           | Restrict to a specific sample (repeatable)       |
| `--model NAME`        | all                           | Restrict to a specific model name (repeatable)   |

#### Output record fields

Every record contains the following metadata fields, parsed from the results path:

```jsonc
{
  "benchmark":   "test_pass_rate" | "complexity",
  "sample":      "AssetPlus",
  "tool":        "ecore" | "umple",
  "model":       "claude_opus_4_7",
  "eval_type":   "controller" | "test",
  "config":      "feat_gen" | "gen" | "feat_dom" | "dom",
  "batch_id":    "msgbatch_...",
  "repetition":  "r1",
  "result_path": "/abs/path/to/results/.../r1",
  "timestamp":   "2026-04-30T22:51:45Z",
  // ...benchmark-specific fields below...
}
```

**`test_pass_rate`** — same fields as the `testpassrate` benchmark above (`pass_count`, `fail_count`, `error_count`, `total_count`, `pass_rate`, `test_cases[]`, `pytest_returncode`). Coverage is included when pytest-cov is available; for test eval it measures the ground-truth controller; for controller eval it measures the generated controller.

**`complexity`** — controller eval only:

```jsonc
{
  // ...metadata fields...
  "benchmark": "complexity",
  "methods": [
    {
      "method": "ClassName.method_name",
      "cyclomatic_complexity": { "total": 5, "rank": "A" },
      "maintainability_index": { "score": 67.04, "rank": "A" },
    },
  ],
  "aggregate": {
    "total_cyclomatic_complexity": 17,
    "avg_cyclomatic_complexity": 5.6667,
    "avg_maintainability_index": 64.75,
  },
}
```

Error records (benchmark failed for a specific entry) include an `"error"` key instead of the normal result fields.

#### Console output

Progress is printed as each entry completes, followed by a summary table:

```text
Found 720 result directories to evaluate.
Output: .../pipeline_results.jsonl

  [1/720] claude_opus_4_7 / ecore / controller / AssetPlus / feat_gen / r1
  ...

Model                                     Mode          Entries
----------------------------------------------------------------
claude_opus_4_7                           controller        120
claude_opus_4_7                           test              120
gpt_5_4                                   controller        120
...
```
