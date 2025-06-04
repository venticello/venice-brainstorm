import json
import os
from datetime import datetime
from typing import Dict, Any

from config import RESULTS_DIR

# Console output settings
CONSOLE_SEPARATOR = "=" * 80

def print_section(title: str):
    """Print a section header"""
    print(f"\n{title}")
    print(CONSOLE_SEPARATOR)


def save_report(report: Dict[str, Any], filename: str = None):
    """Save report to JSON file"""
    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(RESULTS_DIR, f"venice_brainstorm_{timestamp}.json")

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"📁 Report saved: {filename}")

    # Also save readable version
    readable_filename = filename.replace('.json', '_readable.txt')
    with open(readable_filename, 'w', encoding='utf-8') as f:
        f.write(f"AI BRAINSTORM REPORT\n")
        f.write(f"{CONSOLE_SEPARATOR}\n")
        f.write(f"Topic: {report['topic']}\n")
        f.write(f"Date: {report['timestamp']}\n")
        f.write(f"{CONSOLE_SEPARATOR}\n\n")
        f.write(report['final_result'])
        f.write(f"\n\n{CONSOLE_SEPARATOR}\n")
        f.write("TOKEN USAGE SUMMARY\n")
        f.write(f"{CONSOLE_SEPARATOR}\n")
        f.write(f"Total tokens: {report['token_usage'].get('total_tokens', 0)}\n")
        f.write(f"Prompt tokens: {report['token_usage'].get('prompt_tokens', 0)}\n")
        f.write(f"Completion tokens: {report['token_usage'].get('completion_tokens', 0)}\n")

    print(f"📄 Readable version: {readable_filename}")

    # Print token usage summary
    print_section("📊 Token Usage Summary")
    print(f"Total tokens: {report['token_usage'].get('total_tokens', 0)}")
    print(f"Prompt tokens: {report['token_usage'].get('prompt_tokens', 0)}")
    print(f"Completion tokens: {report['token_usage'].get('completion_tokens', 0)}")
