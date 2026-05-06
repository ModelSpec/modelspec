"""Controller generation: build prompts and submit batch jobs."""

from .._shared import (
    DATA_DIR,
    load_configs, read_text, collect_features, stub_controller,
    collect_model_layer, read_domain_model, build_prompt,
)

MODE = "controller"


def build_requests(tools: list[str], configs: list[str], sample: str, rep: int = 1) -> list[dict]:
    """Build all (tool, config) request dicts for controller generation."""
    CONFIGS = load_configs(MODE)

    sample_dir = DATA_DIR / sample
    description = read_text(sample_dir / "description.txt")
    features = collect_features(sample_dir / "features")

    all_requests: list[dict] = []
    for tool in tools:
        tool_dir = sample_dir / tool
        controller_path = tool_dir / "controller" / "controller.py"
        stubbed = stub_controller(controller_path)

        print(f"=== Stubbed controller ({sample}/{tool}) ===")
        print(stubbed)
        print("==========================\n")

        for config_name in configs:
            config = CONFIGS[config_name]
            model_context = (
                collect_model_layer(tool_dir)
                if config.model_type == "gen"
                else read_domain_model(tool_dir, tool)
            )
            prompt = build_prompt(config, stubbed, description, features,
                                  model_context)
            all_requests.append({
                "custom_id": f"{sample}-{tool}-{config_name}-r{rep}",
                "sample": sample,
                "tool": tool,
                "config": config_name,
                "rep": rep,
                "prompt": prompt,
            })

    return all_requests
