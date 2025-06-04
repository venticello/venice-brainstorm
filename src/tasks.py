from typing import List
from crewai import Task

def create_brainstorm_tasks(topic: str, context: str, agents: dict) -> List[Task]:
    """Create tasks for brainstorm on given topic"""
    base_context = f"Brainstorm topic: {topic}\n"
    if context:
        base_context += f"Additional context: {context}\n"

    tasks = []

    # Task 1: Generate creative ideas
    tasks.append(Task(
        description=f"""{base_context}

        Your task as a creative generator:
        1. Propose 5-7 innovative ideas on the given topic
        2. Give a brief but inspiring description for each idea
        3. Don't limit yourself to obvious solutions - think boldly
        4. Use analogies from other fields if it helps
        5. Focus on potential and possibilities, not limitations

        Response format: numbered list of ideas with description of each.""",
        agent=agents['creative'],
        expected_output="List of 5-7 creative ideas with detailed descriptions",
    ))

    # Task 2: Practical analysis
    tasks.append(Task(
        description=f"""{base_context}

        Analyze ideas proposed by the creative generator.

        Your task as a practical analyst:
        1. Evaluate each idea on feasibility criteria (1-10)
        2. Specify main required resources (time, money, people)
        3. Identify main risks and obstacles
        4. Propose concrete steps for implementing top-3 ideas
        5. Give realistic timeline for implementation

        Be constructively critical, but don't kill ideas outright.""",
        agent=agents['analyst'],
        expected_output="Detailed analysis of feasibility of each idea with ratings and action plan"
    ))

    # Task 3: UX analysis
    tasks.append(Task(
        description=f"""{base_context}

        Evaluate proposed ideas from user experience perspective.

        Your task as a UX expert:
        1. Define target audience for each idea
        2. Evaluate usability and accessibility
        3. Predict emotional response of users
        4. Identify potential problems in user experience
        5. Propose improvements to make each idea more user-friendly
        6. Rank ideas by attractiveness to users

        Think as an end user, not as a developer.""",
        agent=agents['ux_expert'],
        expected_output="UX analysis of each idea focusing on user experience and usability"
    ))

    # Task 4: Technical assessment
    tasks.append(Task(
        description=f"""{base_context}

        Conduct technical expertise of proposed ideas.

        Your task as a technical expert:
        1. Evaluate technical complexity of each idea (1-10)
        2. Determine required technologies and tools
        3. Identify technical risks and limitations
        4. Propose alternative technical approaches
        5. Evaluate scalability and performance
        6. Give recommendations on solution architecture

        Be expert but explain complex concepts in simple terms.""",
        agent=agents['tech_expert'],
        expected_output="Technical assessment of each idea with complexity analysis and recommendations"
    ))

    # Task 5: Final analysis and evaluation
    tasks.append(Task(
        description=f"""{base_context}

        Create final report based on all previous analyses.

        Your task as a strategic evaluator:
        1. BRIEF SUMMARY: Essence of all proposed ideas (2-3 paragraphs)

        2. TOP-3 IDEAS with justification:
           - Idea name
           - Why it made it to top
           - Key advantages
           - Main challenges

        3. COMPREHENSIVE BRAINSTORM ASSESSMENT:
           - Creativity (1-10 + justification)
           - Practicality (1-10 + justification)
           - User value (1-10 + justification)
           - Technical feasibility (1-10 + justification)
           - OVERALL RATING (1-10)

        4. STRATEGIC RECOMMENDATIONS:
           - Which idea to implement first
           - Step-by-step action plan
           - Key success metrics
           - Potential partners/resources

        5. NEXT STEPS: Concrete actions for next 30/90 days

        Be objective but inspiring. Focus on actionable recommendations.""",
        agent=agents['evaluator'],
        expected_output="Comprehensive final report with ratings, top ideas and strategic recommendations"
    ))

    return tasks 