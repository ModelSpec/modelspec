# Description Complexity Analyzer

This tool requires PyTorch (AKA `torch`) to run perplexity analyzer. Since `torch` is a large dependency and is not useful for most of the other tools in this repository, it is not included in the default `requirements-dev.txt`. To install it, run `pip install torch`.

Alternatively, you can download PyTorch through [light-the-torch](https://pypi.org/project/light-the-torch/), which speeds up installation exponentially. Refer to the documentation for installation instructions.

Alternatively, use `--disable-perplexity` to skip the perplexity metric.

## What this analyzer does

This analyzer computes cognitive complexity metrics for each sample `description.txt` in `data/`.

The output includes:

- **Readability**: Flesch-Kincaid grade, Dale-Chall score. Estimates baseline reading difficulty from sentence length, word length, and common-word coverage.
- **Syntactic**: dependent clause count, max dependency-tree depth. Estimates grammatical complexity.
- **Lexical**: content token count, average Zipf frequency. Estimates vocabulary sophistication.
- **Semantic cohesion**: average similarity between consecutive sentences. Estimates coherence.
- **Perplexity**: language-model perplexity score. Estimates how surprising the text is, where higher values usually indicate harder or less predictable text.

## Correlation

The directory also includes a `correlation.py` script that computes pairwise correlations between all computed metrics across samples. Although this correlation is **not** a standard metric, it can be useful for understanding how different complexity dimensions relate to each other across samples.
