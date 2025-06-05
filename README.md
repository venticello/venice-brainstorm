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
git clone https://github.com/venticello/venice-brainstorm.git
cd venice-brainstorm
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
cd src
python brainstorm.py
```

### Custom Topic

Run with a custom topic:
```bash
cd src
python brainstorm.py --topic "Your custom topic" --context "Additional context"
```

### Available Options

- `--topic`: Custom topic for brainstorm
- `--context`: Additional context for the topic
- `--template`: Template to use (product, ecology, education, startup)
- `--temperature`: Temperature parameter for LLM (0.0 to 1.0)
- `--top-p`: Top-p parameter for LLM (0.0 to 1.0)
- `--model`: Model to use (list bellow)

### Venice models and context size
- venice-uncensored `32768`
- qwen-2.5-qwq-32b `32768`
- qwen3-4b `32768`
- mistral-31-24b `131072`
- qwen3-235b `32768`
- llama-3.2-3b `131072`
- llama-3.3-70b `65536`
- llama-3.1-405b `65536`
- dolphin-2.9.2-qwen2-72b `32768`
- qwen-2.5-vl `32768`
- qwen-2.5-coder-32b `32768`
- deepseek-r1-671b `131072`
- deepseek-coder-v2-lite `131072`


### Environment Variables

You can configure the following settings in the `.env` file:
- `VENICE_API_KEY`: Your Venice AI API key
- `BRAINSTORM_MODEL`: AI model to use
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

```
.
├── src/
│   ├── brainstorm.py    # Main script
│   ├── agents.py        # Agent definitions
│   ├── tasks.py         # Task definitions
│   ├── templates.py     # Ready-made templates
│   ├── config.py        # Configuration settings
│   └── utils.py         # Utility functions
├── results/             # Directory for output files
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Example

```bash
cd src
python brainstorm.py --template startup
```

This will run a brainstorming session on creating an AI technology startup with a budget of $100k and a 12-month planning horizon.

---

MIT License

