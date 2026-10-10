from agents.resume_parser import resume_parser
from agents.jd_analyzer import jd_analyzer
from agents.skill_matcher import skill_matcher
from agents.ats_scorer import ats_scorer
from agents.feedback_agent import feedback_agent
from agents.interview_agent import interview_agent
from agents.supervisor import supervisor
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


result = supervisor(state)

print("=" * 80)

print("ATS Score")
print(result["overall_score"])

print("=" * 80)

print("Feedback")

print(result["feedback"])

print("=" * 80)

print("Interview Questions")

print(result["interview_questions"])