# ModelSpec: A Dataset and Benchmark for Evaluating LLM-Based Spec-Driven Repository-Level Code Generation

ModelSpec is a dataset and benchmark for evaluating LLMs on domain-model-assisted code generation. Each sample pairs a system description, a domain model (in both [Umple](https://cruise.umple.org/umpleonline/) and [Ecore/Emfatic](https://eclipse.dev/emfatic/) form), Gherkin feature files, a ground-truth controller, and a test suite. The benchmark measures how well LLMs generate the controller and the test suite from these artifacts under different prompting configurations.

## File Structure

```text
modelspec/
├── data/                            # Dataset samples (one folder per system)
│   ├── conftest.py
│   ├── pytest.ini
│   └── <sample>/                    # e.g. AssetPlus, BikeTourPlus, ...
│       ├── description.txt          # Natural-language system description
│       ├── features/                # Gherkin .feature files
│       ├── tests/                   # Ground-truth pytest test suite
│       ├── ecore/
│       │   ├── model/model.emf      # Emfatic source model
│       │   ├── generated_*/         # The idea is that these files are generated, and do not need to be included in the dataset source code. However, due to a few technical limitations, the process is not fully automated, so we are keeping them there for now so that we can access them more easily.
│       │   └── controller/          # Ground-truth controller
│       └── umple/
│           ├── model/model.ump      # Umple source model
│           ├── generated_*/
│           └── controller/          # Ground-truth controller
├── tools/                           # Complementary scripts (each subfolder has its own README)
└── requirements.txt
```

## Setup

Python 3.13+ is required. We recommend setting up a virtual environment and installing the dependencies with:

```bash
pip install -r requirements.txt
```

You will additionally need:

- [Eclipse Modeling Tools](https://www.eclipse.org/downloads/packages/release/2025-09/r/eclipse-modeling-tools) with the [Emfatic](https://eclipse.dev/emfatic/download/) plugin, if you want to edit/generate `.ecore` from `.emf`.
- [Umple](https://cruise.umple.org/umpleonline/download_umple.shtml) — for generating Python model layers from `.ump`.
- API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`) — only if you intend to run `tools/generation_runner` against live LLM APIs.

## How Tos

### Add a New Sample to the Dataset

#### Generate an Umple Model Layer from an Umple (.ump) Model

1. Go to https://cruise.umple.org/umpleonline.
2. Paste your Umple model in the left panel.
3. In `TOOLS` → `GENERATE`, choose `Python Code` and click `Generate It`.
4. The output is a single `.py` file. Split it into a Python package with `tools/umple_file_splitter/` and place the result under `data/<sample>/umple/generated_model_layer/`.

#### Generate an Ecore Model Layer from an Emfatic (.emf) Model

1. Open `Eclipse Modeling Tools` and create or open an `Ecore Modeling Project`.
2. Add your `.emf` file, right-click it, and choose `Generate Ecore Model`. The `.ecore` file lands in `data/<sample>/ecore/generated_ecore_model/`.
3. Use [`pyecoregen`](https://pypi.org/project/pyecoregen/) to produce the Python model layer:

   ```bash
   pyecoregen -vv -e data/<sample>/ecore/generated_ecore_model/model.ecore -o data/<sample>/ecore/generated_model_layer
   ```

### Run Tests

Each sample has a single test suite at `data/<sample>/tests/` that is parametrized over both modeling tools via `data/conftest.py`. The `tools/middleware/` package provides the abstraction that lets the same test exercise either an Umple-generated or an Ecore-generated model layer.

Note that tests depend on both `data` and `tools/middleware` to run.

```bash
# Run all tests in the suite
python -m pytest data

# Run a sample's tests against both modeling tools (default)
python -m pytest data/<sample>/tests

# Restrict to one modeling tool
python -m pytest data/<sample>/tests --modeling-tool ecore
python -m pytest data/<sample>/tests --modeling-tool umple
```

To evaluate an LLM-generated controller or test suite against the ground truth, use `tools/benchmarks/testpassrate` rather than invoking pytest directly — it sets up the import paths and emits a structured JSONL record.

### Get Dataset Statistics

See [tools/analyzers/README.md](tools/analyzers/README.md).

### Send a Generation Request to an LLM API

See [tools/generation_runner/README.md](tools/generation_runner/README.md).

### Evaluate Generated Code

See [tools/benchmarks/README.md](tools/benchmarks/README.md).
