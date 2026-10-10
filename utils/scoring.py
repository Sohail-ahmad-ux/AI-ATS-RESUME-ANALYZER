import re


def percentage(obtained: int, total: int) -> float:
    if total == 0:
        return 100.0

    return round((obtained / total) * 100, 2)


# -----------------------------
# Skill Score
# -----------------------------

def skill_score(matched: list[str], required: list[str]) -> float:

    return percentage(len(matched), len(required))


# -----------------------------
# Experience Score
# -----------------------------

def experience_score(
    resume_experience: str,
    required_experience: str,
) -> float:

    if required_experience.strip() == "":
        return 100

    resume_years = re.findall(r"\d+", resume_experience)

    required_years = re.findall(r"\d+", required_experience)

    if not required_years:
        return 100

    if not resume_years:
        return 30

    resume_years = int(resume_years[0])

    required_years = int(required_years[0])

    if resume_years >= required_years:
        return 100

    return round((resume_years / required_years) * 100, 2)


# -----------------------------
# Education Score
# -----------------------------

def education_score(
    resume_education: str,
    required_education: str,
) -> float:

    if required_education == "":
        return 100

    resume = resume_education.lower()

    required = required_education.lower()

    if "phd" in required:

        if "phd" in resume:
            return 100

        return 60

    if "master" in required:

        if "master" in resume:
            return 100

        if "bachelor" in resume:
            return 80

        return 40

    if "bachelor" in required:

        if "bachelor" in resume:

            return 100

        return 50

    return 80


# -----------------------------
# Resume Quality
# -----------------------------

def resume_quality_score(resume: str):

    score = 0

    if len(resume) > 1000:
        score += 20

    keywords = [
        "project",
        "education",
        "experience",
        "skill",
        "certification",
    ]

    for word in keywords:

        if word.lower() in resume.lower():

            score += 16

    return min(score, 100)


# -----------------------------
# Keyword Score
# -----------------------------

def keyword_score(
    resume: str,
    required_skills: list[str],
):

    if len(required_skills) == 0:
        return 100

    found = 0

    resume = resume.lower()

    for skill in required_skills:

        if skill.lower() in resume:

            found += 1

    return percentage(found, len(required_skills))