"""Configuration settings for the brainstorm application"""

# Default settings
DEFAULT_MODEL = "openai/o1" # venice "llama-3.1-405b"
DEFAULT_TEMPERATURE = 0.8
DEFAULT_TOP_P = 1.0
DEFAULT_BASE_URL = "https://api.venice.ai/api/v1"
DEFAULT_TEMPLATE = "startup"
DEFAULT_RPM = 20
RESULTS_DIR = "results"

# Available models
MODELS = [
    "openai/o1-mini",  # "llama-3.3-70b"
    "openai/o1",       # "llama-3.1-405b"
    "openai/gpt-4.1",  # "qwen3-235b"
]

# Console output settings
CONSOLE_WIDTH = 80
CONSOLE_SEPARATOR = "=" * CONSOLE_WIDTH 