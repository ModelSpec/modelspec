def sanitize_model_name(model_name: str) -> str:
    return (model_name.lower()
            .replace("-", "_")
            .replace(".", "_")
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_"))