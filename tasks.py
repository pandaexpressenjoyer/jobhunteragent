from crewai import Task

def create_tasks(job_searcher, skills_advisor, interview_coach):
    """
    Defines the chronological list of tasks required to execute the pipeline,
    now explicitly capturing and tracking live application URLs.
    """
    task_find_jobs = Task(
        description=(
            "Search and analyze active {target_roles} positions currently open in the {location}. "
            "Focus explicitly on extracting hardware dependencies, software stacks, and development tooling. "
            "Crucially, for each position or pattern you identify, extract and include the exact source links "
            "and application URLs discovered via your search tool so the user can easily find and apply to them."
        ),
        expected_output=(
            "A structured list of core requirements, industry expectations, and critical technical skills, "
            "accompanied by the raw source links and application URLs for the target positions discovered."
        ),
        agent=job_searcher
    )

    task_analyze_skills = Task(
        description=(
            "Review the target technical profiles and application links discovered by the Researcher. "
            "Cross-reference the requirements against this candidate profile: {user_profile}. "
            "Pinpoint critical skill gaps and suggest a practical timeline to bridge them, "
            "preserving the context of which companies required which skills."
        ),
        expected_output="A concise skill gap breakdown paired with specific project or framework learning paths.",
        agent=skills_advisor
    )

    task_coaching = Task(
        description=(
            "Review the gathered job requirements, identified skill gaps, and active job openings. "
            "Synthesize a targeted performance playbook containing 3 highly probable technical "
            "interview questions and evaluation talking points customized for this pipeline.\n\n"
            "At the very bottom of your final output, create a clear section titled '### 🔗 Target Job Postings & Application Links' "
            "and map out a bulleted list of the exact source URLs and job links passed down from the Researcher task "
            "so the candidate has direct access to them."
        ),
        expected_output="3 targeted interview questions complete with ideal engineering response strategies, followed by a dedicated section listing discovered job application URLs.",
        agent=interview_coach,
        output_file="advice.md"  # Saves the clean final report with links included
    )

    # Return the tasks as an ordered list for sequential execution
    return [task_find_jobs, task_analyze_skills, task_coaching]