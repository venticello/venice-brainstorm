"""Configuration settings for the brainstorm application"""

# Default settings
DEFAULT_MODEL = "openai/gpt-4.1" # venice "qwen3-235b"
DEFAULT_TEMPERATURE = 0.75
DEFAULT_TOP_P = 0.9
DEFAULT_BASE_URL = "https://api.venice.ai/api/v1"
DEFAULT_TEMPLATE = "startup"
DEFAULT_RPM = 20 # for small models can be up to 50
RESULTS_DIR = "results"

# Available models
MODELS = [
    "openai/o1-mini",  # "llama-3.3-70b"
    "openai/o1",       # "llama-3.1-405b"
    "openai/gpt-4.1",  # "qwen3-235b"
]

