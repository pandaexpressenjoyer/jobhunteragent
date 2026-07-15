from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

def create_agents(llm_brain):
    """
    Factory function to initialize and return the system's specialized agent team,
    now equipped with live search, web page deep scraping, and ATS tailoring.
    """
    # Initialize real-time data acquisition tools
    web_search_tool = SerperDevTool()
    web_scrape_tool = ScrapeWebsiteTool()

    # Agent 1: Now equipped with web search and scraping to scan active listings
    job_searcher = Agent(
        role="Technical Job Market Researcher",
        goal="Locate relevant open positions and scrape their full requirements using live data.",
        backstory=(
            "An elite tech recruiter who leverages real-time web search and deep webpage "
            "scraping to extract exact full-text engineering requirements from open roles."
        ),
        llm=llm_brain,
        tools=[web_search_tool, web_scrape_tool],  
        verbose=True
    )

    # Agent 2: Remains a pure analytical reasoning engine
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

    # Agent 4: New optimizer engine required by the tabbed desktop interface
    ats_optimizer = Agent(
        role="ATS Resume Optimization Expert",
        goal="Align the candidate's resume structure, keyword distribution, and project descriptions to excel in automated parsing filters.",
        backstory=(
            "A specialized resume engineer who knows how to reframe existing engineering projects "
            "to maximize contextual keyword density for modern Applicant Tracking Systems without fabricating experience."
        ),
        llm=llm_brain,
        verbose=True
    )

    return job_searcher, skills_advisor, interview_coach, ats_optimizer