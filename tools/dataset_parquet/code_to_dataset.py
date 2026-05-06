import json
import pandas as pd
from pathlib import Path


def read_file(path):
    """Read file content as text."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def make_object(sample_path, rel_path):
    """Make a single object with path and code."""
    full_path = sample_path / rel_path
    if not full_path.exists():
        return None
    return {
        "path": str(Path(rel_path)).replace("\\", "/"),
        "code": read_file(full_path)
    }


def make_list(sample_path, rel_folder, pattern):
    """Make a list of objects from a folder."""
    folder = sample_path / rel_folder
    if not folder.exists():
        return None
    files = sorted(folder.glob(pattern))
    if not files:
        return None
    result = []
    for f in files:
        rel = f.relative_to(sample_path)
        result.append({
            "path": str(rel).replace("\\", "/"),
            "code": read_file(f)
        })
    return result


def read_jsonl(path):
    """Read a JSONL file and return a list of records."""
    if not path.exists():
        return None
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records if records else None


def read_metrics_single(path):
    """Read a single-record JSONL file and return just the metrics dict."""
    records = read_jsonl(path)
    if not records:
        return None
    return records[0].get("metrics")


def read_metrics_list(paths):
    """Read one or more JSONL files and return a flat list of simplified records."""
    result = []
    for path in paths:
        records = read_jsonl(path)
        if not records:
            continue
        for r in records:
            item = {}
            if "entity" in r:
                item.update(r["entity"])
            if "metrics" in r:
                item.update(r["metrics"])
            result.append(item)
    return result if result else None


def process_sample(sample_path):
    """Process one sample folder into a row."""
    sample_name = sample_path.name

    # description
    desc_file = sample_path / "description.txt"
    description = read_file(desc_file) if desc_file.exists() else None

    # root __init__.py
    umple_init = make_object(sample_path, Path("__init__.py"))

    # umple
    umple_model_ump = make_object(sample_path, Path("umple/model/model.ump"))
    umple_model_layer = make_list(sample_path, "umple/generated_model_layer", "*.py")
    umple_controller = make_list(sample_path, "umple/controller", "*.py")

    # ecore
    ecore_model_emf = make_object(sample_path, Path("ecore/model/model.emf"))
    ecore_model_ecore = make_object(sample_path, Path("ecore/generated_ecore_model/model.ecore"))
    ecore_model_layer = make_list(sample_path, "ecore/generated_model_layer", "*.py")
    ecore_controller = make_list(sample_path, "ecore/controller", "*.py")

    # features and tests
    features = make_list(sample_path, "features", "*.feature")
    tests = make_list(sample_path, "tests", "*.py")

    # analyzer metrics
    domainmodel_metrics = read_metrics_single(
        sample_path / "domainmodel_metrics.jsonl"
    )
    description_complexity_metrics = read_metrics_single(
        sample_path / "description_complexity_metrics.jsonl"
    )
    controller_metrics = read_metrics_list([
        sample_path / "controller_template_metrics.jsonl"
    ])
    gherkin_metrics = read_metrics_list([
        sample_path / "gherkin_scenario_metrics.jsonl",
        sample_path / "gherkin_background_metrics.jsonl"
    ])

    return {
        "sample_name": sample_name,
        "description": description,
        "umple_init": json.dumps(umple_init) if umple_init else None,
        "umple_model_ump": json.dumps(umple_model_ump) if umple_model_ump else None,
        "umple_model_layer": json.dumps(umple_model_layer) if umple_model_layer else None,
        "umple_controller": json.dumps(umple_controller) if umple_controller else None,
        "ecore_model_emf": json.dumps(ecore_model_emf) if ecore_model_emf else None,
        "ecore_model_ecore": json.dumps(ecore_model_ecore) if ecore_model_ecore else None,
        "ecore_model_layer": json.dumps(ecore_model_layer) if ecore_model_layer else None,
        "ecore_controller": json.dumps(ecore_controller) if ecore_controller else None,
        "features": json.dumps(features) if features else None,
        "tests": json.dumps(tests) if tests else None,
        "domainmodel_metrics": json.dumps(domainmodel_metrics) if domainmodel_metrics else None,
        "description_complexity_metrics": json.dumps(description_complexity_metrics) if description_complexity_metrics else None,
        "controller_metrics": json.dumps(controller_metrics) if controller_metrics else None,
        "gherkin_metrics": json.dumps(gherkin_metrics) if gherkin_metrics else None,
    }


def main():
    repo_root = Path(__file__).parent.parent.parent
    data_dir = repo_root / "data"
    output_path = Path(__file__).parent / "modelspec_dataset.parquet"

    rows = []
    for sample_path in sorted(data_dir.iterdir()):
        if not sample_path.is_dir():
            continue
        if sample_path.name.startswith('.') or sample_path.name.startswith('_'):
            print(f"Skipping {sample_path.name}")
            continue
        print(f"Processing {sample_path.name}...")
        row = process_sample(sample_path)
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_parquet(output_path, index=False)
    print(f"\nDone! Parquet saved to: {output_path}")
    print(f"Total samples: {len(rows)}")


if __name__ == "__main__":
    main()