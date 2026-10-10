from agents.education_matcher import education_matcher

state = {
    "resume_education": "Bachelor of Science in Computer Science",
    "required_education": "Bachelor's Degree in Computer Science"
}

result = education_matcher(state)

print("=" * 40)
print("Education Score")
print(result["education_score"])