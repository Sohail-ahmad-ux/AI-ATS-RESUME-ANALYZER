from langchain_core.prompts import ChatPromptTemplate

from config import llm
from schemas import ResumeInfo
from state import ATSState


resume_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert ATS resume parser.

Extract the candidate information accurately.

If information is missing,
return an empty string or empty list.

Only use information found in the resume.
""",
        ),
        (
            "human",
            """
Resume:

{resume}
""",
        ),
    ]
)

structured_llm = llm.with_structured_output(ResumeInfo)

chain = resume_prompt | structured_llm


def resume_parser(state: ATSState) -> ATSState:
    resume = state["resume_text"]

    result = chain.invoke(
        {
            "resume": resume
        }
    )

    state["candidate_name"] = result.candidate_name
    state["resume_skills"] = result.skills
    state["resume_experience"] = result.experience
    state["resume_education"] = result.education

    return state