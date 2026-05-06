import ast
from pathlib import Path



def find_python_files(directory: Path) -> list[Path]:
    """All .py files directly within a single directory, excluding __init__.py."""
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix == ".py" and p.name != "__init__.py"
    )


def iter_python_sources(directory: Path) -> list[tuple[Path, str]]:
    """Read all .py sources from a single directory (non-recursive, no __init__.py)."""
    return [
        (path, path.read_text(encoding="utf-8", errors="replace"))
        for path in find_python_files(directory)
    ]


def extract_method_sources(source: str) -> list[dict[str, str]]:
    tree = ast.parse(source)
    method_entries: list[dict[str, str]] = []

    def walk(node: ast.AST, class_stack: list[str]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                walk(child, class_stack + [child.name])
                continue

            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if child.name.startswith("_"):
                    continue

                method_name = child.name
                if class_stack:
                    method_name = f"{'.'.join(class_stack)}.{child.name}"

                method_source = ast.get_source_segment(source, child)
                if method_source:
                    method_entries.append({"method": method_name, "source": method_source})

                walk(child, class_stack)

    walk(tree, [])
    return method_entries