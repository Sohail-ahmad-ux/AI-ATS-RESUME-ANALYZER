import streamlit as st


def score_card(score, recommendation):

    color = "#10B981"

    if score < 70:
        color = "#F59E0B"

    if score < 50:
        color = "#EF4444"

    st.markdown(
    f"""
<div class="score-card">

<div class="score-value" style="color:{color};">
    {score:.0f}%
</div>

<div class="score-title">
    ATS Score
</div>

<div class="recommendation">
    {recommendation}
</div>

</div>
""",
    unsafe_allow_html=True,
)