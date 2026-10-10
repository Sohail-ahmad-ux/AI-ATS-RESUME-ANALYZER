import re

from state import ATSState


def extract_years(text: str) -> int:
    """
    Extract the first number of years from text.

    Examples:
    '2+ years' -> 2
    '3 years experience' -> 3
    'one year' -> 0 (can be improved later)
    """

    if not text:
        return 0

    match = re.search(r"(\d+)", text)

    if match:
        return int(match.group(1))

    return 0


def experience_matcher(state: ATSState) -> ATSState:

    resume_years = extract_years(
        state.get("resume_experience", "")
    )

    required_years = extract_years(
        state.get("required_experience", "")
    )

    # No requirement mentioned
    if required_years == 0:

        score = 100.0

    elif resume_years >= required_years:

        score = 100.0

    else:

        score = (resume_years / required_years) * 100

    state["experience_score"] = round(score, 2)

    return state