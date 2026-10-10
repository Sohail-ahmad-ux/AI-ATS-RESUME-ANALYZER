from agents.ats_scorer import ats_scorer

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

    "matched_skills": [
        "Python",
        "LangChain",
        "FastAPI"
    ],

    "missing_skills": [
        "Docker",
        "SQL"
    ],

    "resume_experience": "AI Engineer with ML projects",

    "resume_education": "BS Computer Science"
}

state = ats_scorer(state)

print("=" * 60)
print("Overall Score:", state["overall_score"])
print()

print("Recommendation:")
print(state["recommendation"])
print()

print("Strengths:")
for item in state["strengths"]:
    print("-", item)

print()

print("Weaknesses:")
for item in state["weaknesses"]:
    print("-", item)

print("=" * 60)