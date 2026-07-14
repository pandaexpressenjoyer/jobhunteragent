from crewai import Agent
from crewai_tools import SerperDevTool  

def create_agents(llm_brain):
    """
    Factory function to initialize and return the system's specialized agent team,
    now equipped with live search tools.
    """
    # Initialize the internet search tool instance
    web_search_tool = SerperDevTool()

    # Agent 1: Now equipped with web search to scan active listings
    job_searcher = Agent(
        role="Technical Job Market Researcher",
        goal="Locate relevant open positions that match user criteria using live data.",
        backstory=(
            "An elite tech recruiter who leverages real-time web data to find "
            "high-signal engineering listings and dissect hidden requirements."
        ),
        llm=llm_brain,
        tools=[web_search_tool],  
        verbose=True
    )

    # Agent 2: Remains a pure analytical reasoning engine (no tools needed)
    skills_advisor = Agent(
        role="Technical Skills Gap Analyst",
        goal="Compare job requirements against a user profile to discover gaps and outline direct learning roadmaps.",
        backstory="A systems engineering mentor who knows exactly what tech stacks matter and how to learn them efficiently without fluff.",
        llm=llm_brain,
        verbose=True
    )

    # Agent 3: Remains an outbound interview prep strategy engine
    interview_coach = Agent(
        role="Technical Interview Strategist",
        goal="Generate highly specific technical interview questions based on targeted job descriptions.",
        backstory="A veteran engineering manager who conducts tough but fair technical interviews, focusing heavily on concrete project execution.",
        llm=llm_brain,
        verbose=True
    )

    return job_searcher, skills_advisor, interview_coach