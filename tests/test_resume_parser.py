from agents.resume_parser import resume_parser
from utils.pdf_loader import PDFLoader

state = {
    "resume_text": PDFLoader.extract_text("Sohail_CV.pdf")
}

updated_state = resume_parser(state)

print("=" * 50)
print("Candidate Name:", updated_state["candidate_name"])
print("Skills:", updated_state["resume_skills"])
print("Experience:", updated_state["resume_experience"])
print("Education:", updated_state["resume_education"])
print("=" * 50)