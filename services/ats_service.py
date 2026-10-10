from agents.supervisor import supervisor


def analyze_resume(resume_text, job_description):
    """
    Runs the complete ATS pipeline.
    """

    state = {
        "resume_text": resume_text,
        "job_description": job_description,
    }

    result = supervisor(state)

    return result