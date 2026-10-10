from config import llm
from state import ATSState
from schemas import ATSScoreReport
from langchain_core.prompts import ChatPromptTemplate


def ats_scorer(state: ATSState) -> ATSState:

    skill = state.get("skill_score", 0)

    experience = state.get("experience_score", 0)

    education = state.get("education_score", 0)

    keyword = state.get("keyword_score", 0)

    resume_quality = state.get("resume_quality_score", 0)

    overall = (
        skill * 0.40 +
        experience * 0.20 +
        education * 0.15 +
        keyword * 0.15 +
        resume_quality * 0.10
    )

    state["overall_score"] = round(overall, 2)

    strengths = []

    weaknesses = []

    if skill >= 70:
        strengths.append("Strong skill match")
    else:
        weaknesses.append("Skill gap")

    if experience >= 70:
        strengths.append("Relevant experience")
    else:
        weaknesses.append("Experience below requirement")

    if education >= 70:
        strengths.append("Education matches requirement")
    else:
        weaknesses.append("Education mismatch")

    if keyword >= 70:
        strengths.append("Good ATS keyword coverage")
    else:
        weaknesses.append("Missing ATS keywords")

    if resume_quality >= 70:
        strengths.append("Well-structured resume")
    else:
        weaknesses.append("Resume formatting needs improvement")

    state["strengths"] = strengths
    state["weaknesses"] = weaknesses

    if overall >= 85:
        recommendation = "Strong Fit"

    elif overall >= 70:
        recommendation = "Moderate Fit"

    else:
        recommendation = "Weak Fit"

    state["recommendation"] = recommendation

    return state
