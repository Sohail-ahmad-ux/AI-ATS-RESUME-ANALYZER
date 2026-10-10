from agents.keyword_analyzer import keyword_analyzer

state = {
    "resume_text": """
Python
FastAPI
Git
LangChain
REST API
""",
    "required_skills": [
        "Python",
        "FastAPI",
        "Docker",
        "SQL",
        "LangChain",
        "Git"
    ]
}

result = keyword_analyzer(state)

print("=" * 40)
print("Keyword Score")
print(result["keyword_score"])