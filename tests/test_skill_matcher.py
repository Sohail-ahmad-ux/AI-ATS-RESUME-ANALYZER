from agents.skill_matcher import skill_matcher

state = {
    "resume_skills": [
        "Python",
        "LangChain",
        "FastAPI",
        "Git",
        "PyTorch"
    ],
    "required_skills": [
        "Python",
        "LangChain",
        "Docker",
        "SQL",
        "FastAPI"
    ]
}

state = skill_matcher(state)

print("=" * 50)
print("Matched:", state["matched_skills"])
print("Missing:", state["missing_skills"])
print("Score:", state["match_score"])
print("=" * 50)