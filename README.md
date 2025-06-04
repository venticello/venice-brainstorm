# AI Brainstorm with VeniceAI

This project implements an AI-powered brainstorming system using the CrewAI framework. It creates a team of specialized AI agents that work together to generate, analyze, and evaluate ideas on a given topic.

## Features

- Team of specialized AI agents:
  - Creative Idea Generator
  - Practical Analyst
  - UX Expert
  - Technical Expert
  - Strategic Evaluator
- Structured brainstorming process
- Token usage tracking
- Ready-made templates for common topics
- Detailed reports in both JSON and readable formats
- Support for Venice AI models

## Prerequisites

- Python 3.8 or higher
- Venice AI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Venice AI API key:
```
VENICE_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Run the script with a default template:
```bash
python brainstorm.py
```

### Custom Topic

Run with a custom topic:
```bash
python brainstorm.py --topic "Your custom topic" --context "Additional context"
```

### Available Options

- `--topic`: Custom topic for brainstorm
- `--context`: Additional context for the topic
- `--template`: Template to use (product, ecology, education, startup)
- `--temperature`: Temperature parameter for LLM (0.0 to 1.0)
- `--top-p`: Top-p parameter for LLM (0.0 to 1.0)
- `--model`: Model to use (openai/o1-mini, openai/o1, openai/gpt-4.1)

### Models Compatibility Mappings
-   "openai/o1-mini" -> "llama-3.3-70b"
-   "openai/o1"      -> "llama-3.1-405b"
-   "openai/gpt-4.1"  -> "qwen3-235b"

### Environment Variables

You can configure the following settings in the `.env` file:
- `VENICE_API_KEY`: Your Venice AI API key
- `VENICE_MODEL`: Default model to use
- `VENICE_TEMPERATURE`: Default temperature setting
- `VENICE_TOP_P`: Default top-p setting

## Output

The script generates two types of output files in the `results` directory:
1. JSON report (`venice_brainstorm_TIMESTAMP.json`)
2. Readable text report (`venice_brainstorm_TIMESTAMP_readable.txt`)

The reports include:
- Topic and context
- Results from each agent
- Final evaluation and recommendations
- Token usage statistics

## Project Structure

- `brainstorm.py`: Main script
- `agents.py`: Agent definitions
- `tasks.py`: Task definitions
- `templates.py`: Ready-made templates
- `config.py`: Configuration settings
- `requirements.txt`: Project dependencies
- `results/`: Directory for output files

## Example

```bash
python brainstorm.py --template startup
```

This will run a brainstorming session on creating an AI technology startup with a budget of $100k and a 12-month planning horizon.

---

MIT License

