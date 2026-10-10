from graph import graph
from utils.pdf_loader import PDFLoader

state = {
    "resume_text": PDFLoader.extract_text("Sohail_CV.pdf"),
    "job_description": """
AI Engineer

Requirements

Python

LangChain

Machine Learning

Deep Learning

SQL

Docker

FastAPI

Experience:
2+ years developing AI applications.

Education:
Bachelor's degree in Computer Science.
"""
}

result = graph.invoke(state)

print("=" * 60)
print("Candidate:", result["candidate_name"])
print()

print("Match Score:", result["match_score"])
print("Overall Score:", result["overall_score"])
print()

print("Matched Skills:")
for skill in result["matched_skills"]:
    print("-", skill)

print()

print("Missing Skills:")
for skill in result["missing_skills"]:
    print("-", skill)

print()

print("Recommendation:")
print(result["recommendation"])

print("=" * 60)