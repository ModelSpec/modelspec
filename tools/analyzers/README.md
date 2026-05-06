# Analyzers

This directory contains standalone analyzers that compute metrics from sample projects in `data/`.

Analyzers produce **JSONL** output (a special type of JSON file with one JSON object per line). _The description similarity analyzer is a exception as it produces a **CSV** matrix._

All analyzer scripts support these options:

- `--data-dir`: input root (defaults to the repository `data/` directory).
- `--output-dir`: output root directory (defaults to `--data-dir`).
- `--output-name`: output filename.
- `--clean`: delete this analyzer's generated output(s) and exit.

For **JSONL analyzers**, outputs are written per sample as:

- `<output-dir>/<sample-name>/<output-name>`

This means by default, JSONL metrics are written into each sample directory under `data/`.

## Usage Examples

```bash
cd tools/analyzers
python main.py
python main.py --clean
python main.py --run-description-similarity
python main.py --run-description-similarity --clean
python main.py --data-dir ../../data --output-dir ../../data
python main.py --keywords-file domainmodel/attributes/reviewed_keywords.json
python -m gherkin.analyzer --output-dir gherkin
python -m gherkin.analyzer --clean
python -m controllertemplate.analyzer --data-dir data --output-dir .
python -m domainmodel.analyzer
python -m domainmodel.attributes.analyzer
```

## Run All

`main.py` runs all top-level analyzers in parallel using subshells.

It is meant to be used to populate samples with metadata. Thus, by default, it does not run the `description.similarity.analyzer` since it produces a single matrix output. Use `--run-description-similarity` to include it explicitly.

### Shared arguments

- `--data-dir`: shared input root for all analyzers (default: repository `data/`).
- `--output-dir`: shared output root for all analyzers. If omitted, each analyzer keeps its own default output location.
- `--clean`: run selected analyzers in clean mode to delete their generated outputs.

### Analyzer-specific pass-through arguments

- `--controller-output-name`
- `--gherkin-output-name`
- `--domainmodel-output-name`
- `--keywords-file`
- `--description-complexity-output-name`
- `--sentence-model`
- `--spacy-model`
- `--perplexity-model`
- `--disable-perplexity`
- `--run-description-similarity`
- `--description-similarity-output-name`
- `--description-similarity-model`

## Index

- `controllertemplate.analyzer`
  - Controller methods, controller input arguments per method.
  - Default output: `controller_template_metrics.jsonl`
- `description.complexity.analyzer`
  - Has specific installation instructions (see its README).
  - NLP-based complexity metrics from `description.txt` files.
  - Default output: `description_complexity_metrics.jsonl`
- `description.similarity.analyzer`
  - Pairwise semantic similarity between `description.txt` files.
  - Default output: `description_similarity_matrix.csv`
  - Not run by `main.py` unless `--run-description-similarity` is set.
- `domainmodel.analyzer`
  - Aggregates all domain model metrics from the sub-analyzers.
  - Default output: `domainmodel_metrics.jsonl`
  - We expect the emfatic model to have the same values, thus we only run the analyzer on the Umple model files.
  - `domainmodel.file.analyzer`
    - computes file-size metrics (number of characters, lines).
    - Default output: `domainmodel_file_metrics.jsonl`
  - `domainmodel.class.analyzer`
    - computes concrete class, abstract class, and enum metrics.
    - Default output: `domainmodel_class_metrics.jsonl`
  - `domainmodel.relationships.analyzer`
    - computes inheritance, associations (uni/bidirectional), and compositions relationship metrics.
    - Default output: `domainmodel_relationships_metrics.jsonl`
  - `domainmodel.attributes.analyzer`
    - computes attribute counts.
    - to simplify the script, it uses a `reviewed_keyword.json` file to determine which keywords are reserved (i.e. do not count as attributes), which is currently curated by prompting the user to review new keywords.
    - Default output: `domainmodel_attributes_metrics.jsonl`
- `gherkin.analyzer`
  - computes scenario and step metrics from `.feature` files.
  - Default outputs: `gherkin_scenario_metrics.jsonl`, `gherkin_background_metrics.jsonl`
