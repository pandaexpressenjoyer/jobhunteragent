from crewai import Agent

def create_agents(llm_brain):
    """
    Factory function to initialize and return the system's specialized agent team.
    """
    job_searcher = Agent(
        role="Technical Job Market Researcher",
        goal="Locate relevant open positions that match user criteria.",
        backstory="An elite recruiter who knows how to spot high-signal engineering listings and dissect hidden requirements.",
        llm=llm_brain,
        verbose=True
    )

    skills_advisor = Agent(
        role="Technical Skills Gap Analyst",
        goal="Compare job requirements against a user profile to discover gaps and outline direct learning roadmaps.",
        backstory="A systems engineering mentor who knows exactly what tech stacks matter and how to learn them efficiently without fluff.",
        llm=llm_brain,
        verbose=True
    )

    interview_coach = Agent(
        role="Technical Interview Strategist",
        goal="Generate highly specific technical interview questions based on targeted job descriptions.",
        backstory="A veteran engineering manager who conducts tough but fair technical interviews, focusing heavily on concrete project execution.",
        llm=llm_brain,
        verbose=True
    )

    return job_searcher, skills_advisor, interview_coach