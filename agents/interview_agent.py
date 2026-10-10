from prompts.interview_prompt import INTERVIEW_PROMPT
from config import llm


def interview_agent(state):
    """
    Generate interview questions based on the resume
    and job description.
    """

    chain = INTERVIEW_PROMPT | llm

    response = chain.invoke(
        {
            "context": state["resume_text"],
            "job_description": state["job_description"],
        }
    )

    state["interview_questions"] = response.content

    return state