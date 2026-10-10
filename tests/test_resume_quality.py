from agents.resume_quality_analyzer import resume_quality_analyzer

state = {
    "resume_text": """
John Smith

Python
FastAPI
LangChain
Machine Learning

Education

BS Computer Science

Projects

AI ATS
RAG Chatbot
"""
}

result = resume_quality_analyzer(state)

print("=" * 40)

print("Resume Quality Score")

print(result["resume_quality_score"])