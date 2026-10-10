from agents.interview_agent import interview_agent
from utils.pdf_loader import PDFLoader

resume = PDFLoader.extract_text("Sohail_CV.pdf")

state = {
    "resume_text": resume,
    "job_description": """
AI Engineer

Required Skills

Python
LangChain
FastAPI
Docker
SQL
Deep Learning
"""
}

result = interview_agent(state)

with open("outputs/interview_questions.txt", "w", encoding="utf-8") as f:
    f.write(result["interview_questions"])

print("Interview questions saved successfully!")