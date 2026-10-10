from typing import TypedDict


class ATSState(TypedDict, total=False):

    # ==========================
    # Input
    # ==========================
    resume_text: str
    job_description: str

    # ==========================
    # Resume Information
    # ==========================
    candidate_name: str
    resume_skills: list[str]
    resume_experience: str
    resume_education: str

    # ==========================
    # Job Description
    # ==========================
    required_skills: list[str]
    required_experience: str
    required_education: str

    # ==========================
    # Skill Matching
    # ==========================
    matched_skills: list[str]
    missing_skills: list[str]

    # ==========================
    # Detailed Scores
    # ==========================
    skill_score: float
    experience_score: float
    education_score: float
    keyword_score: float
    resume_quality_score: float
    overall_score: float

    # NEW
    resume_completeness_score: float

    # ==========================
    # Candidate Analysis
    # ==========================
    candidate_summary: str

    strengths: list[str]
    weaknesses: list[str]

    # ==========================
    # Final ATS
    # ==========================
    overall_score: float
    recommendation: str

    # ==========================
    # Output
    # ==========================
    feedback: str
    interview_questions: str