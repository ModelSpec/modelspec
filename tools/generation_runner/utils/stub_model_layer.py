"""
tools/generation_runner/utils/stub_model_layer.py

Stubs a Python model-layer source file down to signatures only:
imports, class names, class attributes, function/method signatures,
decorators, and nested classes are preserved.  Method bodies, arbitrary
top-level code, and comments are removed.

Usage:
    python -m tools.generation_runner.utils.stub_model_layer <path/to/model.py>
"""
import ast
import sys


def _signature_lines(node: ast.AST, lines: list[str]) -> list[str]:
    """Return source lines for decorators + def/class signature (excluding body)."""
    result: list[str] = []
    if hasattr(node, "decorator_list"):
        for dec in node.decorator_list:
            for ln in range(dec.lineno, dec.end_lineno + 1):
                result.append(lines[ln - 1])
    body_start = node.body[0].lineno if node.body else node.end_lineno + 1
    if body_start > node.lineno:
        sig: list[str] = []
        for ln in range(node.lineno, body_start):
            sig.append(lines[ln - 1])
        # Strip trailing blank/comment lines that sit between the
        # signature and the first body statement.
        while sig and (not sig[-1].strip() or sig[-1].strip().startswith("#")):
            sig.pop()
        result.extend(sig)
    else:
        # Body on same line as def/class – keep up to the colon.
        line = lines[node.lineno - 1]
        result.append(line[: line.rindex(":") + 1])
    return result


def _process_class_body(class_node: ast.ClassDef, lines: list[str]) -> list[str]:
    """Collect stub lines for a class body (attributes, method sigs, nested classes)."""
    result: list[str] = []
    has_content = False
    for item in class_node.body:
        if isinstance(item, (ast.Assign, ast.AnnAssign)):
            for ln in range(item.lineno, item.end_lineno + 1):
                result.append(lines[ln - 1])
            has_content = True
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if has_content:
                result.append("")
            result.extend(_signature_lines(item, lines))
            has_content = True
        elif isinstance(item, ast.ClassDef):
            if has_content:
                result.append("")
            result.extend(_signature_lines(item, lines))
            result.extend(_process_class_body(item, lines))
            has_content = True
    return result


def stub_model_source(source: str) -> str:
    """Accept a Python source string and return a signature-only stub."""
    tree = ast.parse(source)
    lines = source.splitlines()
    result: list[str] = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for ln in range(node.lineno, node.end_lineno + 1):
                result.append(lines[ln - 1])
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result.append("")
            result.extend(_signature_lines(node, lines))
        elif isinstance(node, ast.ClassDef):
            result.append("")
            result.extend(_signature_lines(node, lines))
            result.extend(_process_class_body(node, lines))

    text = "\n".join(result).strip()
    return text + "\n" if text else ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m tools.generation_runner.utils.stub_model_layer <file.py>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        source = f.read()
    print(stub_model_source(source), end="")
