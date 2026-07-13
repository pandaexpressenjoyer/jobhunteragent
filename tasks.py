from crewai import Task

def create_tasks(job_searcher, skills_advisor, interview_coach):
    """
    Defines the chronological list of tasks required to execute the pipeline.
    """
    task_find_jobs = Task(
        description=(
            "Search and analyze what core technical skills are currently highest "
            "in demand for {target_roles} positions in {location}. Focus explicitly "
            "on hardware dependencies, software stacks, and development tooling."
        ),
        expected_output="A structured list of core requirements, industry expectations, and critical technical skills.",
        agent=job_searcher
    )

    task_analyze_skills = Task(
        description=(
            "Review the target technical profiles discovered by the Researcher. "
            "Cross-reference them against this candidate profile: {user_profile}. "
            "Pinpoint critical skill gaps and suggest a practical timeline to bridge them."
        ),
        expected_output="A concise skill gap breakdown paired with specific project or framework learning paths.",
        agent=skills_advisor
    )

    task_coaching = Task(
        description=(
            "Review the gathered job requirements and identified skill gaps. "
            "Synthesize a targeted performance playbook containing 3 highly probable technical "
            "interview questions and evaluation talking points customized for this pipeline."
        ),
        expected_output="3 targeted interview questions complete with ideal engineering response strategies and tips.",
        agent=interview_coach
    )

    # Return the tasks as an ordered list for sequential execution
    return [task_find_jobs, task_analyze_skills, task_coaching]