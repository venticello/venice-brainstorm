from typing import Dict
from crewai import Agent, LLM

def create_agents(llm: LLM, max_rpm: int = 20) -> Dict[str, Agent]:
    """Create a team of agents with different roles"""
    agents = {}

    # Creative idea generator
    agents['creative'] = Agent(
        role='Creative Idea Generator',
        goal='Generate innovative and unconventional ideas to solve given tasks',
        backstory="""You are a creative thinker with rich imagination and ability 
        to see unconventional solutions. You draw inspiration from art, nature, and 
        interdisciplinary approaches. Your strength is thinking outside the box 
        and proposing revolutionary ideas.""",
        verbose=True,
        llm=llm,
        max_iter=3,
        max_rpm=max_rpm
    )

    # Practical analyst
    agents['analyst'] = Agent(
        role='Practical Analyst',
        goal='Analyze proposed ideas for feasibility and effectiveness',
        backstory="""You are an experienced business analyst with strong critical 
        thinking skills. You can quickly identify potential problems, assess 
        resources and time costs. Your task is to turn creative ideas into 
        working solutions.""",
        verbose=True,
        llm=llm,
        max_iter=3,
        max_rpm=max_rpm
    )

    # UX expert
    agents['ux_expert'] = Agent(
        role='UX/User Experience Expert',
        goal='Evaluate ideas from user experience and usability perspective',
        backstory="""You are a user experience expert with deep understanding of 
        human psychology and behavior. You always put the user at the center of 
        attention and can predict how people will interact with the solution. 
        Your goal is to make any idea maximally useful for people.""",
        verbose=True,
        llm=llm,
        max_iter=3,
        max_rpm=max_rpm
    )

    # Technical expert
    agents['tech_expert'] = Agent(
        role='Technical Expert',
        goal='Evaluate technical feasibility of ideas and propose technological solutions',
        backstory="""You are a senior technical specialist with years of experience 
        in developing and implementing complex systems. You understand modern 
        technologies, their limitations and capabilities. Your task is to ensure 
        that proposed solutions are technically feasible and scalable.""",
        verbose=True,
        llm=llm,
        max_iter=3,
        max_rpm=max_rpm
    )

    # Strategic evaluator (final analysis)
    agents['evaluator'] = Agent(
        role='Strategic Evaluator',
        goal='Conduct final analysis of all ideas and provide comprehensive assessment',
        backstory="""You are an experienced strategic consultant who can synthesize 
        different perspectives and provide objective assessment. You see the big 
        picture and can predict long-term consequences of decisions. Your task is 
        to create a final report with practical recommendations.""",
        verbose=True,
        llm=llm,
        max_iter=3,
        max_rpm=max_rpm
    )

    return agents 