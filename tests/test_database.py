from database.db import (
    create_table,
    save_candidate,
    get_candidates
)

create_table()

dummy = {

    "candidate_name": "Sohail Ahmad",

    "overall_score": 85,

    "recommendation": "Strong Fit",

    "matched_skills": [

        "Python",

        "FastAPI"

    ],

    "missing_skills": [

        "Docker"

    ],

    "feedback": "Excellent Resume",

    "interview_questions": "Question 1"

}

save_candidate(dummy)

print(get_candidates())