from langchain_core.prompts import ChatPromptTemplate

from config import llm
from schemas import FeedbackReport
from state import ATSState


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert ATS resume reviewer.

Your task is to provide detailed and actionable feedback.

Focus on:

- Missing technical skills
- Resume formatting
- Missing ATS keywords
- Projects to improve
- Certifications
- Ways to increase ATS score

Be practical and specific.
"""
        ),
        (
            "human",
            """
Resume Skills:
{resume_skills}

Required Skills:
{required_skills}

Missing Skills:
{missing_skills}

Experience:
{experience}

Education:
{education}
"""
        ),
    ]
)

structured_llm = llm.with_structured_output(FeedbackReport)

chain = prompt | structured_llm


def feedback_agent(state: ATSState) -> ATSState:

    result = chain.invoke(
        {
            "resume_skills": state["resume_skills"],
            "required_skills": state["required_skills"],
            "missing_skills": state["missing_skills"],
            "experience": state["resume_experience"],
            "education": state["resume_education"],
        }
    )

    state["feedback"] = result.feedback

    return state