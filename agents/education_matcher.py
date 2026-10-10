from state import ATSState


def education_matcher(state: ATSState) -> ATSState:

    resume = state.get("resume_education", "").lower()

    required = state.get("required_education", "").lower()

    if not required:
        score = 100.0

    elif resume == required:
        score = 100.0

    elif required in resume:
        score = 100.0

    elif resume in required:
        score = 90.0

    elif "computer science" in resume and "computer science" in required:
        score = 100.0

    elif "bachelor" in resume and "bachelor" in required:
        score = 80.0

    elif "master" in resume and "bachelor" in required:
        score = 100.0

    else:
        score = 40.0

    state["education_score"] = round(score, 2)

    return state