from crewai import Task

def create_tasks(job_searcher, skills_advisor, interview_coach, ats_optimizer):
    """
    Defines the chronological list of tasks required to execute the pipeline,
    configured to generate structured tokens for the interactive GUI cards.
    """
    task_find_jobs = Task(
        description=(
            "Search and identify active {target_roles} positions open in the {location}. "
            "Use your scraping tool to read the full text of promising listings. Extract hardware dependencies, "
            "software stacks, and development tooling. Include the exact application URLs found."
        ),
        expected_output="A structured list of core requirements, company stacks, and source links derived from full-text job page scrapes.",
        agent=job_searcher
    )

    task_analyze_skills = Task(
        description=(
            "Review the full technical requirements discovered by the Researcher. "
            "Cross-reference them against this candidate profile parsed from their PDF: {user_profile}. "
            "Pinpoint critical skill gaps and suggest a practical timeline to bridge them."
        ),
        expected_output="A concise skill gap breakdown paired with specific project or framework learning paths.",
        agent=skills_advisor
    )

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
        output_file="gta_firmware_playbook.md"
    )

    # Task 4: Tailors resume content into a syntax layout parsable by the GUI
    task_tailor_resume = Task(
        description=(
            "Review the active requirements scraped from the job market and the candidate's original resume text: {user_profile}.\n\n"
            "Identify the top 4-6 most critical keyword or phrase improvements needed to maximize ATS compliance. "
            "For every single improvement, write it out exactly in this structured markdown block format so the GUI can parse it into cards:\n\n"
            "START_SUGGESTION\n"
            "SECTION: [Name of resume section, e.g., Technical Skills Matrix or Game Boy Emulator Project]\n"
            "ISSUE: [Brief description of the missing context or missing keyword, e.g., Missing critical FreeRTOS keyword]\n"
            "CORRECTION: [Detailed text bubble explaining exactly how to reframe or rewrite the bullet point to pass the ATS filter safely]\n"
            "END_SUGGESTION\n\n"
            "Do not deviate from this syntax block. Ensure your corrections focus strictly on contextual keyword density "
            "without fabricating any unearned experience."
        ),
        expected_output="A series of structured suggestion tokens mapping explicit section, issue, and correction attributes.",
        agent=ats_optimizer,
        output_file="ats_optimized_resume.md"
    )

    return [task_find_jobs, task_analyze_skills, task_coaching, task_tailor_resume]