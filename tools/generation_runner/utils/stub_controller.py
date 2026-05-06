"""
stub_controller.py

For the first class in the file, removes private helper methods (single
leading underscore) and stubs public methods. Dunder methods are kept intact.
Public callables outside that class are removed.

Public methods are replaced with:

    # TODO: implement <method_name>
    pass

Usage:
    python stub_controller.py <path/to/controller.py>
"""
import ast
import sys


def _node_start_line(node: ast.AST) -> int:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.decorator_list:
        return min(dec.lineno for dec in node.decorator_list)
    return node.lineno


def stub_source(source: str) -> str:
    """Accept a Python source string and return the stubbed version."""
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)

    class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    if not class_nodes:
        return source

    target_class = class_nodes[0]

    # Operation tuple: (start_lineno, end_lineno, replacement_lines)
    ops = []

    # Remove top-level public functions (outside any class).
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            ops.append((_node_start_line(node), node.end_lineno, []))

    # Remove public methods from non-target classes.
    for class_node in class_nodes[1:]:
        class_public_methods_to_remove = []
        for item in class_node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if item.name.startswith("__") and item.name.endswith("__"):
                continue
            if not item.name.startswith("_"):
                class_public_methods_to_remove.append(item)

        if not class_public_methods_to_remove:
            continue

        removed_ids = {id(item) for item in class_public_methods_to_remove}
        remaining_items = []
        for item in class_node.body:
            if id(item) not in removed_ids:
                remaining_items.append(item)

        if not remaining_items and class_node.body:
            class_def_line = lines[class_node.lineno - 1]
            class_indent = len(class_def_line) - len(class_def_line.lstrip())
            pass_indent = " " * (class_indent + 4)
            body_start = min(_node_start_line(child) for child in class_node.body)
            body_end = class_node.body[-1].end_lineno
            ops.append((body_start, body_end, [f"{pass_indent}pass\n"]))
        else:
            for method_node in class_public_methods_to_remove:
                ops.append((_node_start_line(method_node), method_node.end_lineno, []))

    # Process methods in the target class.
    for item in target_class.body:
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if item.name.startswith("__") and item.name.endswith("__"):
            continue

        if item.name.startswith("_"):
            ops.append((_node_start_line(item), item.end_lineno, []))
            continue

        def_line = lines[item.lineno - 1]
        method_indent = len(def_line) - len(def_line.lstrip())
        body_indent = " " * (method_indent + 4)
        body_start = item.body[0].lineno
        body_end = item.end_lineno
        stub = [
            f"{body_indent}# TODO: implement {item.name}\n",
            f"{body_indent}pass\n",
        ]
        ops.append((body_start, body_end, stub))

    # Apply in reverse order so original line positions remain valid.
    ops.sort(key=lambda x: x[0], reverse=True)
    for start, end, replacement in ops:
        lines[start - 1 : end] = replacement

    return "".join(lines)


def stub_public_methods(filepath: str) -> None:
    """Read a file, stub it in place, and print a summary."""
    with open(filepath, encoding="utf-8") as f:
        source = f.read()

    result = stub_source(source)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Stubbed controller written to: {filepath}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stub_controller.py <controller.py path>")
        sys.exit(1)
    stub_public_methods(sys.argv[1])
