from agents.feedback_agent import feedback_agent

state = {
    "resume_skills": [
        "Python",
        "LangChain",
        "FastAPI",
        "PyTorch"
    ],

    "required_skills": [
        "Python",
        "LangChain",
        "Docker",
        "SQL",
        "FastAPI"
    ],

    "missing_skills": [
        "Docker",
        "SQL"
    ],

    "resume_experience": """
AI Engineer with Machine Learning projects.
Built LangChain applications.
""",

    "resume_education": """
BS Computer Science
"""
}

state = feedback_agent(state)

print("=" * 60)
print(state["feedback"])
print("=" * 60)