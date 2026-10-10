from agents.jd_analyzer import jd_analyzer

state = {
    "job_description": """
AI Engineer

Requirements:

- Python
- LangChain
- Machine Learning
- Deep Learning
- SQL
- Docker
- FastAPI

Experience:
2+ years developing AI applications.

Education:
Bachelor's degree in Computer Science.
"""
}

state = jd_analyzer(state)

print("=" * 50)
print(state["required_skills"])
print(state["required_experience"])
print(state["required_education"])
print("=" * 50)