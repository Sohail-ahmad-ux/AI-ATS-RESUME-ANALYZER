from langchain_core.prompts import ChatPromptTemplate

from config import llm
from schemas import JobDescriptionInfo
from state import ATSState


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an ATS Job Description Analyzer.

Extract:

- Required Skills
- Required Experience
- Required Education

Return only information that actually appears in the job description.
"""
        ),
        (
            "human",
            """
Job Description:

{job_description}
"""
        ),
    ]
)

structured_llm = llm.with_structured_output(JobDescriptionInfo)

chain = prompt | structured_llm


def jd_analyzer(state: ATSState) -> ATSState:

    result = chain.invoke(
        {
            "job_description": state["job_description"]
        }
    )

    state["required_skills"] = result.required_skills
    state["required_experience"] = result.required_experience
    state["required_education"] = result.required_education

    return state