from pydantic import BaseModel, Field


class ResumeInfo(BaseModel):
    """
    Structured information extracted from a resume.
    """

    candidate_name: str = Field(
        description="Full name of the candidate"
    )

    skills: list[str] = Field(
        description="Technical and soft skills"
    )

    experience: str = Field(
        description="Work experience summary"
    )

    education: str = Field(
        description="Highest education"
    )

from pydantic import BaseModel, Field


class JobDescriptionInfo(BaseModel):
    """
    Structured information extracted from a job description.
    """

    required_skills: list[str] = Field(
        default_factory=list,
        description="Technical and soft skills required for the job"
    )

    required_experience: str = Field(
        default="",
        description="Required years or type of experience"
    )

    required_education: str = Field(
        default="",
        description="Required education"
    )
class JDInfo(BaseModel):
    """
    Structured information extracted from
    a job description.
    """

    required_skills: list[str] = Field(
        description="Skills required for the job"
    )

    required_experience: str = Field(
        description="Experience required"
    )


class MatchResult(BaseModel):
    """
    Result of comparing the resume with
    the job description.
    """

    matched_skills: list[str]

    missing_skills: list[str]

    match_score: float


class FeedbackResult(BaseModel):
    """
    Resume improvement suggestions.
    """

    feedback: str


class InterviewQuestions(BaseModel):
    """
    Interview questions generated for the candidate.
    """

    questions: list[str]

class ATSScoreReport(BaseModel):
    """
    AI evaluation of the candidate.
    """

    overall_score: float = Field(
        description="Overall ATS score from 0 to 100"
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Candidate strengths"
    )

    weaknesses: list[str] = Field(
        default_factory=list,
        description="Candidate weaknesses"
    )

    recommendation: str = Field(
        description="Strong Fit, Moderate Fit, or Weak Fit"
    )

class FeedbackReport(BaseModel):
    """
    Resume improvement suggestions.
    """

    feedback: str = Field(
        description="Detailed resume improvement suggestions."
    )

class ResumeQualityReport(BaseModel):
    """
    AI evaluation of resume quality.
    """

    score: float = Field(
        description="Resume quality score from 0 to 100"
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Resume strengths"
    )

    improvements: list[str] = Field(
        default_factory=list,
        description="Areas needing improvement"
    )