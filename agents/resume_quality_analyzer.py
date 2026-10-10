from langchain_core.prompts import ChatPromptTemplate

from config import llm
from schemas import ResumeQualityReport
from state import ATSState

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an ATS Resume Expert.

Evaluate the resume ONLY.

Score from 0 to 100 based on:

• Formatting
• Readability
• Section organization
• ATS friendliness
• Professional appearance

Do not compare against the job description.

Return structured output.
"""
        ),
        (
            "human",
            """
Resume

{resume}
"""
        ),
    ]
)

structured_llm = llm.with_structured_output(
    ResumeQualityReport
)

chain = prompt | structured_llm


def resume_quality_analyzer(state: ATSState) -> ATSState:

    result = chain.invoke(
        {
            "resume": state["resume_text"]
        }
    )

    state["resume_quality_score"] = result.score

    return state