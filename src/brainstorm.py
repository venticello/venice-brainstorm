import os
import argparse
from datetime import datetime
from typing import Dict, Any

from crewai import Crew, Process, LLM
from dotenv import load_dotenv

# Disable telemetry
os.environ["OTEL_SDK_DISABLED"] = "true"

from config import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE,
    DEFAULT_BASE_URL, DEFAULT_TEMPLATE, DEFAULT_RPM,
    MODELS,MODELS_CONTEXT
)
from agents import create_agents
from tasks import create_brainstorm_tasks
from templates import BRAINSTORM_TEMPLATES
from utils import print_section, save_report

# Load environment variables
load_dotenv()


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
            top_p: Optional top-p parameter for LLM (0.0 to 1.0)
        """
        # Get API key from environment or parameter
        self.api_key = api_key or os.getenv("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Set it via api_key parameter or VENICE_API_KEY environment variable")

        # Get model from environment or parameter
        self.model = model or os.getenv("BRAINSTORM_MODEL", DEFAULT_MODEL)
        if not self.model:
            raise ValueError("Model not specified")

        # Get temperature from environment or parameter
        self.temperature = temperature or float(os.getenv("VENICE_TEMPERATURE", str(DEFAULT_TEMPERATURE)))
        if not 0 <= self.temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")

        # Get top_p from environment or parameter
        self.top_p = top_p or os.getenv("VENICE_TOP_P")
        if self.top_p is not None:
            self.top_p = float(self.top_p)
            if not 0 <= self.top_p <= 1:
                raise ValueError("Top-p must be between 0 and 1")

        # Check model availability
        if self.model not in MODELS:
            raise ValueError(f"Unsupported model: {self.model}. Available models: {', '.join(MODELS)}")
        try:
            self.llm = LLM(
                model=f"openai/{self.model}",
                temperature=self.temperature,
                top_p=self.top_p,
                base_url=base_url,
                api_key=self.api_key,
            )
            self.llm.context_window_size = MODELS_CONTEXT.get(self.model, 0)
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM: {str(e)}")

        self.agents = {}
        self.tasks = []

    def create_agents(self):
        """Create a team of agents with different roles"""
        self.agents = create_agents(self.llm, DEFAULT_RPM)

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
            name="Venice brainstorm",
            agents=list(self.agents.values()),
            tasks=self.tasks,
            process=Process.sequential,  # Sequential task execution
            verbose=True,
            # output_log_file=True
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
            'token_usage': usage_metrics,
            'model': self.model
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


def main():
    """Main function to run brainstorm"""
    parser = argparse.ArgumentParser(description='Run AI Brainstorm session')
    parser.add_argument('--topic', type=str, help='Custom topic for brainstorm')
    parser.add_argument('--context', type=str, help='Additional context for the topic')
    parser.add_argument('--template', type=str, choices=list(BRAINSTORM_TEMPLATES.keys()),
                       default=DEFAULT_TEMPLATE, help='Template to use if no custom topic provided')
    parser.add_argument('--temperature', type=float, help='Temperature parameter for LLM (0.0 to 1.0)')
    parser.add_argument('--top-p', type=float, help='Optional top-p parameter for LLM (0.0 to 1.0)')
    parser.add_argument('--model', type=str, help='Model to use')
    
    args = parser.parse_args()

    # Print configuration
    print_section("🔧 Configuration")
    print(f"Model: {args.model or os.getenv('BRAINSTORM_MODEL', DEFAULT_MODEL)}")
    print(f"Temperature: {args.temperature or os.getenv('VENICE_TEMPERATURE', str(DEFAULT_TEMPERATURE))}")
    if args.top_p or os.getenv("VENICE_TOP_P"):
        print(f"Top-p: {args.top_p or os.getenv('VENICE_TOP_P')}")
    print(f"Base URL: {DEFAULT_BASE_URL}")

    # Initialize with Venice AI
    brainstorm_crew = AIBrainstormCrew(
        api_key=os.getenv("VENICE_API_KEY"),
        model=args.model or os.getenv("BRAINSTORM_MODEL", DEFAULT_MODEL),
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
        report_path = save_report(report)

        print_section("🎉 BRAINSTORM COMPLETE")
        print("Check generated result: \n", report_path)

    except Exception as e:
        print(f"❌ Error during brainstorm: {e}")
        print("Check:")
        print("1. Venice AI API key correctness")
        print("2. Internet connection availability")
        print("3. All dependencies installation")


if __name__ == "__main__":
    main()