SYSTEM_PROMPT = "You are a senior Python developer."


def api_for_model(model: str) -> str:
    """Return 'openai', 'anthropic', or 'google' based on the model name prefix."""
    if model.startswith("gpt-"):
        return "openai"
    if model.startswith("claude-"):
        return "anthropic"
    if model.startswith("gemini-"):
        return "google"
    if model.startswith("gemma-"):
        return "openrouter_direct"
    raise ValueError(f"Cannot determine API for model '{model}'. "
                     "Expected prefix 'gpt-', 'claude-', 'gemini-', or 'gemma-'.")