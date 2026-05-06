# Gherkin Analyzer

## Output

Two JSONL files are written:

- Scenario output: `gherkin_scenario_metrics.jsonl`. Gives the metrics for each scenario.
- Background output: `gherkin_background_metrics.jsonl`. Gives the metrics for each background (mostly just the number of Givens).

## Success/Failure Estimation

Given the amount of steps in the dataset, we want to have an automatic method to estimate the number of success/failure scenarios without having to manually label them.

Heuristically, the analyzer attempts to estimate whether a scenario is a success or failure based on the presence of failure-related keywords in the scenario's steps. If any step contains keywords like "raise", "throw", "error", "exception", "failure", or "fail", the scenario is marked as a failure. If a step contains "throw no exception" or "not throw exception", it is marked as a success. The default behavior assumes success if no failure indicators are found.
