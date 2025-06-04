import json
import os
from datetime import datetime

def print_section(title: str):
    """Print a section title with formatting"""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50 + "\n")

def save_report(report: dict):
    """Save brainstorm report in JSON and readable formats"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save JSON report
    json_path = f"results/venice_brainstorm_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Save readable report
    txt_path = f"results/venice_brainstorm_{timestamp}_readable.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"AI Brainstorm Report\n")
        f.write(f"===================\n\n")
        f.write(f"Topic: {report['topic']}\n")
        if report['context']:
            f.write(f"Context: {report['context']}\n")
        f.write(f"Timestamp: {report['timestamp']}\n")
        f.write(f"Agents Used: {', '.join(report['agents_used'])}\n\n")
        
        f.write("Task Results\n")
        f.write("------------\n")
        for task in report['task_results']:
            f.write(f"\nTask {task['task_number']} ({task['agent']}):\n")
            f.write(f"{task['result']}\n")
        
        f.write("\nFinal Result\n")
        f.write("------------\n")
        f.write(f"{report['final_result']}\n")
        
        f.write("\nToken Usage\n")
        f.write("-----------\n")
        f.write(f"Total Tokens: {report['token_usage']['total_tokens']}\n")
        f.write(f"Prompt Tokens: {report['token_usage']['prompt_tokens']}\n")
        f.write(f"Completion Tokens: {report['token_usage']['completion_tokens']}\n") 