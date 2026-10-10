from langchain_core.prompts import ChatPromptTemplate


INTERVIEW_PROMPT = ChatPromptTemplate.from_template("""
You are a Senior AI Engineer.

Using the resume and job description, generate interview questions.

Resume:
{context}

Job Description:
{job_description}

Generate:

- 5 Technical Questions
- 3 Machine Learning Questions
- 3 Python Questions
- 2 System Design Questions
- 2 Behavioral Questions

Also provide ideal answers in brief.
""")