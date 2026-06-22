class LiteLLMStartError(Exception):
    """Raised when the LiteLLM proxy fails to start or become ready."""
    pass


class LiteLLMConfigError(Exception):
    """Raised when required config keys are missing or invalid."""
    pass
