from state import ATSState


def keyword_analyzer(state: ATSState) -> ATSState:
    """
    Analyze ATS keyword matching between
    resume and job description.
    """

    resume_text = state.get("resume_text", "").lower()

    required_skills = [
        skill.lower().strip()
        for skill in state.get("required_skills", [])
    ]

    matched = 0

    for skill in required_skills:

        if skill in resume_text:
            matched += 1

    if required_skills:

        score = (matched / len(required_skills)) * 100

    else:

        score = 100

    state["keyword_score"] = round(score, 2)

    return state