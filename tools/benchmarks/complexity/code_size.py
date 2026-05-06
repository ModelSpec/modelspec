"""
Count non-comment lines and characters of code across Python source files.

Uses the tokenizer instead of ast so that inline comments
(e.g. ``func()  # note``) are handled correctly: only the characters
before the ``#`` are counted, and the line still contributes to LOC.
"""

import io
import tokenize
from pathlib import Path


def compute_code_size(sources: list[tuple[Path, str]]) -> dict[str, int]:
    """
    Aggregate lines-of-code and characters-of-code across all (path, source) pairs.
    Comments and blank lines are excluded from both counts.
    """
    total_loc = 0
    total_chars = 0
    for _, source in sources:
        loc, chars = _count_source(source)
        total_loc += loc
        total_chars += chars
    return {"lines_of_code": total_loc, "characters_of_code": total_chars}


def _count_source(source: str) -> tuple[int, int]:
    # Map line number -> column where the comment token starts on that line.
    comment_col: dict[int, int] = {}
    try:
        for tok_type, _, (srow, scol), _, _ in tokenize.generate_tokens(
            io.StringIO(source).readline
        ):
            if tok_type == tokenize.COMMENT:
                comment_col[srow] = scol
    except tokenize.TokenError:
        pass

    loc = 0
    chars = 0
    for i, line in enumerate(source.splitlines(), 1):
        if i in comment_col:
            # Inline comment: keep only the code portion before the '#'.
            code_part = line[: comment_col[i]].strip()
        else:
            code_part = line.strip()
        if code_part:
            loc += 1
            chars += len(code_part)
    return loc, chars
