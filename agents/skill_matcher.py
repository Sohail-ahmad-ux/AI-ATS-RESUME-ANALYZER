from state import ATSState
from config import llm


def skill_matcher(state: ATSState) -> ATSState:

    resume_skills = {
        skill.lower().strip()
        for skill in state.get("resume_skills", [])
    }

    required_skills = {
        skill.lower().strip()
        for skill in state.get("required_skills", [])
    }

    matched = sorted(resume_skills & required_skills)

    missing = sorted(required_skills - resume_skills)

    if required_skills:
        score = (len(matched) / len(required_skills)) * 100
    else:
        score = 0.0

    state["matched_skills"] = matched
    state["missing_skills"] = missing
    state["match_score"] = round(score, 2)
    state["skill_score"] = round(score, 2)

    return state