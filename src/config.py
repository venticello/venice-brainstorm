"""Configuration settings for the brainstorm application"""

# Default settings
DEFAULT_MODEL = "venice-uncensored" # venice "qwen3-235b"
DEFAULT_TEMPERATURE = 0.75
DEFAULT_BASE_URL = "https://api.venice.ai/api/v1"
DEFAULT_TEMPLATE = "startup"
DEFAULT_RPM = 20 # for small models can be up to 50
RESULTS_DIR = "results"


MODELS_CONTEXT = {
  "venice-uncensored": 32768,
  "qwen-2.5-qwq-32b": 32768,
  "qwen3-4b": 32768,
  "mistral-31-24b": 131072,
  "qwen3-235b": 32768,
  "llama-3.2-3b": 131072,
  "llama-3.3-70b": 65536,
  "llama-3.1-405b": 65536,
  "dolphin-2.9.2-qwen2-72b": 32768,
  "qwen-2.5-vl": 32768,
  "qwen-2.5-coder-32b": 32768,
  "deepseek-r1-671b": 131072,
  "deepseek-coder-v2-lite": 131072,
  # "nemotron-8b-ultralong-1M": 1024000
}
# Available models
MODELS = MODELS_CONTEXT.keys()

