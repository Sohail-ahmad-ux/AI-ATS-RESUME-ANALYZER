from agents.ats_agent import ats_agent

state = {
    "resume_path": "Sohail_CV.pdf",
    "job_description": """
AI Engineer

Python

LangChain

FastAPI

Docker

SQL

Deep Learning
"""
}

result = ats_agent(state)

print("=" * 70)

print(result["ats_report"])

print("=" * 70)