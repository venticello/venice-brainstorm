import os
import json
import argparse
from datetime import datetime
from typing import Dict, Any

from crewai import Crew, Process, LLM
from crewai.tools import tool, BaseTool
from dotenv import load_dotenv

from config import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_TOP_P,
    DEFAULT_BASE_URL, DEFAULT_TEMPLATE, DEFAULT_RPM,
    RESULTS_DIR, MODELS, CONSOLE_SEPARATOR
)
from agents import create_agents
from tasks import create_brainstorm_tasks
from templates import BRAINSTORM_TEMPLATES

# Load environment variables
load_dotenv()

def print_section(title: str):
    """Print a section header"""
    print(f"\n{title}")
    print(CONSOLE_SEPARATOR)

@tool
def brainstorm_results(results: str) -> str:
    """Saves and formats brainstorm session results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(RESULTS_DIR, f"brainstorm_results_{timestamp}.txt")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(results)

    return f"Results saved to {filename}"


class AIBrainstormCrew:
    def __init__(self, api_key: str = None, model: str = None,
                 base_url: str = DEFAULT_BASE_URL,
                 temperature: float = None,
                 top_p: float = None):
        """
        Initialize AI Brainstorm using CrewAI

        Args:
            api_key: Venice AI API key
            model: Model to use
            base_url: Base URL for Venice AI API
            temperature: Temperature parameter for LLM (0.0 to 1.0)
            top_p: Top-p parameter for LLM (0.0 to 1.0)
        """
        # Get API key from environment or parameter
        self.api_key = api_key or os.getenv("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Set it via api_key parameter or VENICE_API_KEY environment variable")

        # Get model from environment or parameter
        self.model = model or os.getenv("VENICE_MODEL", DEFAULT_MODEL)
        if not self.model:
            raise ValueError("Model not specified")

        # Get temperature from environment or parameter
        self.temperature = temperature or float(os.getenv("VENICE_TEMPERATURE", str(DEFAULT_TEMPERATURE)))
        if not 0 <= self.temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")

        # Get top_p from environment or parameter
        self.top_p = top_p or float(os.getenv("VENICE_TOP_P", str(DEFAULT_TOP_P)))
        if not 0 <= self.top_p <= 1:
            raise ValueError("Top-p must be between 0 and 1")

        # Check model availability
        if self.model not in MODELS:
            raise ValueError(f"Unsupported model: {self.model}. Available models: {', '.join(MODELS)}")

        try:
            self.llm = LLM(
                model=self.model,
                temperature=self.temperature,
                top_p=self.top_p,
                base_url=base_url,
                api_key=self.api_key
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM: {str(e)}")

        self.agents = {}
        self.tasks = []
        self.results_tool: BaseTool = brainstorm_results

    def create_agents(self):
        """Create a team of agents with different roles"""
        self.agents = create_agents(self.llm, DEFAULT_RPM)
        # Add results tool to evaluator
        self.agents['evaluator'].tools = [self.results_tool]

    def create_brainstorm_tasks(self, topic: str, context: str = ""):
        """Create tasks for brainstorm on given topic"""
        self.tasks = create_brainstorm_tasks(topic, context, self.agents)

    def run_brainstorm(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Run full brainstorm process"""

        print_section("🧠 STARTING AI BRAINSTORM")
        print(f"📋 Topic: {topic}")
        print(f"👥 Participants: {list(self.agents.keys())}")

        # Create tasks
        self.create_brainstorm_tasks(topic, context)

        # Create and run crew
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            process=Process.sequential,  # Sequential task execution
            verbose=True
        )

        # Execute brainstorm
        result = crew.kickoff()

        # Convert UsageMetrics to dictionary
        usage_metrics = {
            'total_tokens': getattr(crew.usage_metrics, 'total_tokens', 0),
            'prompt_tokens': getattr(crew.usage_metrics, 'prompt_tokens', 0),
            'completion_tokens': getattr(crew.usage_metrics, 'completion_tokens', 0)
        }

        # Form final report
        report = {
            'topic': topic,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'agents_used': list(self.agents.keys()),
            'final_result': str(result),
            'task_results': [],
            'token_usage': usage_metrics
        }

        # Collect results of each task
        for i, task in enumerate(self.tasks):
            if hasattr(task, 'output') and task.output:
                task_result = {
                    'task_number': i + 1,
                    'agent': task.agent.role,
                    'result': str(task.output)
                }
                report['task_results'].append(task_result)

        return report

    def save_report(self, report: Dict[str, Any], filename: str = None):
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


def main():
    """Main function to run brainstorm"""
    parser = argparse.ArgumentParser(description='Run AI Brainstorm session')
    parser.add_argument('--topic', type=str, help='Custom topic for brainstorm')
    parser.add_argument('--context', type=str, help='Additional context for the topic')
    parser.add_argument('--template', type=str, choices=list(BRAINSTORM_TEMPLATES.keys()),
                       default=DEFAULT_TEMPLATE, help='Template to use if no custom topic provided')
    parser.add_argument('--temperature', type=float, help='Temperature parameter for LLM (0.0 to 1.0)')
    parser.add_argument('--top-p', type=float, help='Top-p parameter for LLM (0.0 to 1.0)')
    parser.add_argument('--model', type=str, help='Model to use')
    
    args = parser.parse_args()

    # Print configuration
    print_section("🔧 Configuration")
    print(f"Model: {args.model or os.getenv('VENICE_MODEL', DEFAULT_MODEL)}")
    print(f"Temperature: {args.temperature or os.getenv('VENICE_TEMPERATURE', str(DEFAULT_TEMPERATURE))}")
    print(f"Top-p: {args.top_p or os.getenv('VENICE_TOP_P', str(DEFAULT_TOP_P))}")
    print(f"Base URL: {DEFAULT_BASE_URL}")

    # Initialize with Venice AI
    brainstorm_crew = AIBrainstormCrew(
        api_key=os.getenv("VENICE_API_KEY"),
        model=args.model or os.getenv("VENICE_MODEL", DEFAULT_MODEL),
        base_url=DEFAULT_BASE_URL,
        temperature=args.temperature,
        top_p=args.top_p
    )

    # Create agents
    brainstorm_crew.create_agents()

    # Choose topic (can use ready template or custom topic)
    if args.topic:
        template = {
            'topic': args.topic,
            'context': args.context or ''
        }
    else:
        template = BRAINSTORM_TEMPLATES[args.template]

    print_section("🚀 Starting Brainstorm")
    print(f"📋 Topic: {template['topic']}")
    if template['context']:
        print(f"📝 Context: {template['context']}")

    try:
        # Run brainstorm
        report = brainstorm_crew.run_brainstorm(
            topic=template['topic'],
            context=template['context']
        )

        # Save results
        brainstorm_crew.save_report(report)

        print_section("🎉 BRAINSTORM COMPLETE")
        print("Check generated result files.")

    except Exception as e:
        print(f"❌ Error during brainstorm: {e}")
        print("Check:")
        print("1. Venice AI API key correctness")
        print("2. Internet connection availability")
        print("3. All dependencies installation")


if __name__ == "__main__":
    main()