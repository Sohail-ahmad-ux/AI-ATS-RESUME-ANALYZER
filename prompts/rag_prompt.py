from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert ATS recruiter.

Use ONLY the retrieved resume context.

Resume Context:
{context}

Job Description:
{job_description}

Generate:

1. ATS Score (/100)
2. Matching Skills
3. Missing Skills
4. Strengths
5. Weaknesses
6. Recommendation

Do not invent information.
"""
)