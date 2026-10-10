from agents.resume_parser import resume_parser
from agents.jd_analyzer import jd_analyzer
from agents.skill_matcher import skill_matcher
from agents.experience_matcher import experience_matcher
from agents.education_matcher import education_matcher
from agents.keyword_analyzer import keyword_analyzer
from agents.resume_quality_analyzer import resume_quality_analyzer
from agents.ats_scorer import ats_scorer
from agents.feedback_agent import feedback_agent
from agents.interview_agent import interview_agent


def supervisor(state):

    print("\n" + "=" * 70)
    print("STARTING ATS PIPELINE")
    print("=" * 70)

    # ==========================================================
    # Resume Parser
    # ==========================================================

    state = resume_parser(state)

    print("\n================ Resume Skills ================")
    print(state.get("resume_skills"))

    # ==========================================================
    # JD Analyzer
    # ==========================================================

    state = jd_analyzer(state)

    print("\n================ Required Skills ================")
    print(state.get("required_skills"))

    # ==========================================================
    # Skill Matcher
    # ==========================================================

    state = skill_matcher(state)

    print("\n================ Matched Skills ================")
    print(state.get("matched_skills"))

    print("\n================ Missing Skills ================")
    print(state.get("missing_skills"))

    print("\nSkill Score:", state.get("skill_score"))

    # ==========================================================
    # Experience Matcher
    # ==========================================================

    state = experience_matcher(state)

    print("Experience Score:", state.get("experience_score"))

    # ==========================================================
    # Education Matcher
    # ==========================================================

    state = education_matcher(state)

    print("Education Score:", state.get("education_score"))

    # ==========================================================
    # Keyword Analyzer
    # ==========================================================

    state = keyword_analyzer(state)

    print("Keyword Score:", state.get("keyword_score"))

    # ==========================================================
    # Resume Quality Analyzer
    # ==========================================================

    state = resume_quality_analyzer(state)

    print("Resume Quality Score:", state.get("resume_quality_score"))

    # ==========================================================
    # ATS Scorer
    # ==========================================================

    state = ats_scorer(state)

    print("\n================ FINAL ATS =================")
    print("Overall Score:", state.get("overall_score"))
    print("Recommendation:", state.get("recommendation"))
    print("Strengths:", state.get("strengths"))
    print("Weaknesses:", state.get("weaknesses"))

    # ==========================================================
    # Feedback
    # ==========================================================

    state = feedback_agent(state)

    # ==========================================================
    # Interview Questions
    # ==========================================================

    state = interview_agent(state)

    print("\n" + "=" * 70)
    print("ATS PIPELINE COMPLETED")
    print("=" * 70)

    return state