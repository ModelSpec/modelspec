# Generation Runner

A LLM code generation runner for ModelSpec experiments:

1. **Controller generation**: generate the controller implementation.
2. **Test generation**: generate the pytest test suite.

Supports OpenAI, Anthropic, Google (Gemini), and OpenRouter (Gemma) providers.

---

## Directory Structure

```text
generation_runner/
├── submit.py               # CLI: submit generation jobs to LLM APIs
├── check.py                # CLI: poll job status and save results
├── _shared.py              # Shared constants, dataclasses, utilities
├── controller/             # Controller generation logic
│   ├── submit.py           # Build controller prompts
│   └── check.py            # Parse controller responses
├── test/                   # Test generation logic
│   ├── submit.py           # Build test prompts
│   └── check.py            # Parse test responses
├── providers/                 # LLM provider integrations
│   ├── openai.py              # OpenAI Batch API
│   ├── anthropic.py           # Anthropic Message Batches API
│   ├── google.py              # Google GenAI Batch API (for Gemini)
│   ├── openrouter_direct.py   # OpenRouter direct API (parallel, for Gemma)
│   └── misc.py                # System prompt + model-to-provider routing
├── prompts/                # Prompt templates
│   ├── controller/
│   └── test/
├── utils/
│   ├── stub_controller.py  # Stubs public controller methods
│   ├── stub_model_layer.py # Reduces model layer to signatures
|   └── misc.py             # Small utilities
└── batches/                # Runtime: batch metadata (auto-managed)
```

## Usage

### Step 1 — Submit jobs

```bash
# All models, all tools, all configs, all samples (1 repetition each)
python -m tools.generation_runner.submit controller

# Specific model, tool, and config
python -m tools.generation_runner.submit controller gpt-5.4-nano --tool umple --config feat_gen

# Multiple filters, multiple repetitions
python -m tools.generation_runner.submit test --tool umple --config gen --sample AssetPlus --repetitions 3

# Multiple values per flag
python -m tools.generation_runner.submit controller --config feat_gen --config gen --sample Foo --sample Bar
```

**Arguments:**

| Argument            | Description                            | Default                                                        |
| ------------------- | -------------------------------------- | -------------------------------------------------------------- |
| `mode`              | `controller` or `test`                 | required                                                       |
| `models`            | Model name(s)                          | `gpt-5.4`, `gpt-5.4-nano`, `claude-opus-4-7`, `gemma-4-31b-it` |
| `--tool, -t`        | `umple` or `ecore` (repeatable)        | all tools                                                      |
| `--config, -c`      | Generation config (repeatable)         | all configs                                                    |
| `--sample, -s`      | Sample folder name (repeatable)        | all samples in `data/`                                         |
| `--repetitions, -r` | Repetitions per (sample, tool, config) | `1`                                                            |

### Step 2 — Poll for results

```bash
python -m tools.generation_runner.check
```

Run this periodically until all pending batches are complete. Completed batches are automatically parsed and saved; their metadata files are removed from `batches/`.

---

## Generation Configs

Each config controls what context is included in the prompt:

| Config     | Description             | Features | Model context                      |
| ---------- | ----------------------- | -------- | ---------------------------------- |
| `feat_gen` | Full context            | Yes      | Generated model layer (signatures) |
| `gen`      | Minimal context         | No       | Generated model layer (signatures) |
| `feat_dom` | Domain model + features | Yes      | Raw domain model file              |
| `dom`      | Domain model only       | No       | Raw domain model file              |

---

## Output Structure

Results are saved under `results/`:

```text
results/{sample}/{tool}/{sanitized_model}/{mode}/{config}/{batch_id}/r{rep}/
├── raw_response.txt    # Full LLM output
├── system_prompt.txt   # System prompt used (audit)
├── user_prompt.txt     # User prompt used (audit)
├── controller.py       # (controller mode) Generated implementation
└── test*.py            # (test mode) Generated test files
```

---

## Providers

Model names are routed to providers automatically:

| Prefix     | Provider                  | Notes                                                                          |
| ---------- | ------------------------- | ------------------------------------------------------------------------------ |
| `gpt-*`    | OpenAI Batch API          | 24h completion window                                                          |
| `claude-*` | Anthropic Message Batches | Async polling                                                                  |
| `gemini-*` | Google GenAI Batch API    | Async polling                                                                  |
| `gemma-*`  | OpenRouter Direct API     | Gemma not available on Google's batch API; OpenRouter requests run in parallel |

---

## Environment Variables

| Variable             | Required for      |
| -------------------- | ----------------- |
| `OPENAI_API_KEY`     | OpenAI models     |
| `ANTHROPIC_API_KEY`  | Anthropic models  |
| `GOOGLE_API_KEY`     | Gemini models     |
| `OPENROUTER_API_KEY` | Gemma models      |

---

## Workflow Summary

1. `submit` discovers samples, builds prompts, groups requests by API, submits batch jobs, and writes metadata to `batches/`.
2. Batch jobs process asynchronously in the cloud (minutes to hours; Gemma models are processed immediately in parallel via OpenRouter).
3. `check` reads batch metadata, polls each provider, downloads completed results, parses `<file name="...">...</file>` tags from responses, and saves individual files.
4. Each request's results directory also contains the exact prompts used for reproducibility.
