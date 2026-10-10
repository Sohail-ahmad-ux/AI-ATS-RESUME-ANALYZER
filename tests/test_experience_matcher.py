from agents.experience_matcher import experience_matcher

state = {
    "resume_experience": "Worked as AI Engineer for 1 year.",
    "required_experience": "2+ years experience required."
}

result = experience_matcher(state)

print("=" * 40)
print("Experience Score")
print(result["experience_score"])