from crewai import Task

def create_tasks(job_searcher, skills_advisor, interview_coach, ats_optimizer):
    """
    Assembles the chronological task dependencies for the system pipeline.
    Directs tool execution criteria and maps discrete file outputs for final reports.
    """
    # Task 1: Find matching target records and parse their internal contents
    task_find_jobs = Task(
        description=(
            "Search and identify active {target_roles} positions open in the {location}. "
            "Use your scraping tool to read the full text of promising listings. Extract hardware dependencies, "
            "software stacks, and development tooling. Include the exact application URLs found."
        ),
        expected_output="A structured list of core requirements, company stacks, and source links derived from full-text job page scrapes.",
        agent=job_searcher
    )

    # Task 2: Cross-reference required competencies against candidate background
    task_analyze_skills = Task(
        description=(
            "Review the full technical requirements discovered by the Researcher. "
            "Cross-reference them against this candidate profile parsed from their PDF: {user_profile}. "
            "Pinpoint critical skill gaps and suggest a practical timeline to bridge them."
        ),
        expected_output="A concise skill gap breakdown paired with specific project or framework learning paths.",
        agent=skills_advisor
    )

    # Task 3: Build behavioral-technical performance preparation files
    task_coaching = Task(
        description=(
            "Review the gathered job requirements, identified skill gaps, and active job openings. "
            "Synthesize a targeted performance playbook containing 3 highly probable technical "
            "interview questions and evaluation talking points customized for this pipeline.\n\n"
            "At the very bottom, add a clear section titled '### 🔗 Target Job Postings & Application Links' "
            "listing the exact source URLs found by the Researcher."
        ),
        expected_output="3 targeted interview questions complete with ideal engineering response strategies, followed by a dedicated section listing discovered job application URLs.",
        agent=interview_coach,
        output_file="advice.md"
    )

    # Task 4: Reformat documentation fields to clear programmatic candidate screens
    task_tailor_resume = Task(
        description=(
            "Review the active requirements scraped from the job market and the candidate's original resume text: {user_profile}.\n\n"
            "Provide a complete, revised version of the candidate's core resume sections (Technical Skills Matrix and Project Bullets) "
            "optimized to clear automated ATS scanning software for these specific targets.\n\n"
            "Focus on contextual keyword density (ensuring skills like RTOS, CMake, or CAN are naturally aligned) "
            "and suggest high-signal technical vocabulary adjustments (e.g., noting that their Game Boy opcode decoder is an ISA implementation) "
            "without fabricating any new or unearned experience."
        ),
        expected_output="A completely tailored, clean markdown document detailing exact resume section upgrades and keyword adjustments.",
        agent=ats_optimizer,
        output_file="ats_optimized_resume.md"
    )

    return [task_find_jobs, task_analyze_skills, task_coaching, task_tailor_resume]