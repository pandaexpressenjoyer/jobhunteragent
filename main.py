import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# =====================================================================
# 1. ENVIRONMENT ENVIRONMENT CONFIGURATION & MODEL INITIALIZATION
# =====================================================================

# Load environment variables from a local security file (.env)
load_dotenv()

# Define the central large language model brain that drives all agents
# CrewAI routes this through an abstracted LLM class provider
claude_brain = LLM(
    model="anthropic/claude-3-5-sonnet",
    temperature=0.7
)


# =====================================================================
# 2. AGENT DEFINITIONS (PERSONAS & OBJECTIVES)
# =====================================================================

# Agent 1: Primary Data Gathering & Discovery
job_searcher = Agent(
    role="Technical Job Market Researcher",
    goal="Locate relevant open positions that match user criteria.",
    backstory="An elite recruiter who knows how to spot high-signal engineering listings and dissect hidden requirements.",
    llm=claude_brain,
    verbose=True  # Enables terminal console execution tracking logging
)

# Agent 2: Analytical & Comparative Evaluation
skills_advisor = Agent(
    role="Technical Skills Gap Analyst",
    goal="Compare job requirements against a user profile to discover gaps and outline direct learning roadmaps.",
    backstory="A systems engineering mentor who knows exactly what tech stacks matter and how to learn them efficiently without fluff.",
    llm=claude_brain,
    verbose=True
)

# Agent 3: Outbound Strategy & Deliverable Formatting
interview_coach = Agent(
    role="Technical Interview Strategist",
    goal="Generate highly specific technical interview questions based on targeted job descriptions.",
    backstory="A veteran engineering manager who conducts tough but fair technical interviews, focusing heavily on concrete project execution.",
    llm=claude_brain,
    verbose=True
)


# =====================================================================
# 3. TASK DEFINITIONS (THE SEQUENTIAL WORKFLOW ACTIONS)
# =====================================================================

# Step 1: Initialize raw research discovery
task_find_jobs = Task(
    description=(
        "Search and analyze what core technical skills are currently highest "
        "in demand for {target_roles} positions in {location}. Focus explicitly "
        "on hardware dependencies, software stacks, and development tooling."
    ),
    expected_output="A structured list of core requirements, industry expectations, and critical technical skills.",
    agent=job_searcher
)

# Step 2: Comparative context translation (Consumes output from Step 1)
task_analyze_skills = Task(
    description=(
        "Review the target technical profiles discovered by the Researcher. "
        "Cross-reference them against this candidate profile: {user_profile}. "
        "Pinpoint critical skill gaps and suggest a practical timeline to bridge them."
    ),
    expected_output="A concise skill gap breakdown paired with specific project or framework learning paths.",
    agent=skills_advisor
)

# Step 3: Actionable output synthesis (Consumes output from Step 2)
task_coaching = Task(
    description=(
        "Review the gathered job requirements and identified skill gaps. "
        "Synthesize a targeted performance playbook containing 3 highly probable technical "
        "interview questions and evaluation talking points customized for this pipeline."
    ),
    expected_output="3 targeted interview questions complete with ideal engineering response strategies and tips.",
    agent=interview_coach
)


# =====================================================================
# 4. CREW ASSEMBLY & ORCHESTRATION PIPELINE
# =====================================================================

# Bind the individual components together into an executing ecosystem
job_hunting_crew = Crew(
    agents=[job_searcher, skills_advisor, interview_coach],
    tasks=[task_find_jobs, task_analyze_skills, task_coaching],
    process=Process.sequential  # Forces chronological, pipeline execution
)


# =====================================================================
# 5. EXECUTION MATRIX & INPUT KEYWORD INJECTION
# =====================================================================

# Define runtime parameters mapped directly to the bracketed tokens {} in the tasks
execution_inputs = {
    "target_roles": "Embedded Software & Firmware Engineering Internships",
    "location": "Greater Toronto Area",
    "user_profile": (
        "3rd-year Computer Engineering student. Proficient in C/C++ and Python. "
        "Experienced with bare-metal microcontrollers (SPI/I2C), writing low-level "
        "hardware emulators, and signal analysis using Digilent WaveForms. "
        "Lacks production RTOS (Real-Time Operating System) or Linux kernel driver experience."
    )
}

if __name__ == "__main__":
    print("\n==============================================")
    print("🚀 INITIALIZING MULTI-AGENT ORCHESTRATION...")
    print("==============================================\n")
    
    # Run the system pipeline
    final_report = job_hunting_crew.kickoff(inputs=execution_inputs)
    
    print("\n==============================================")
    print("✨ PIPELINE COMPLETE. GENERATED CONSOLIDATED REPORT:")
    print("==============================================\n")
    print(final_report)