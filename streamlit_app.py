import tempfile
import streamlit as st

from utils.pdf_report import generate_report
from services.ats_service import analyze_resume

from components.charts import (
    skill_pie_chart,
    score_bar_chart,
    ats_gauge,
)

from database.db import create_table
from utils.pdf_loader import PDFLoader

from components.header import render_header
from components.score_card import score_card
from components.skill_cards import skill_cards
from components.feedback_card import feedback_card
from components.interview_card import interview_card
from components.stats_card import stats_card


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    try:
        with open("static/style.css", "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )
    except FileNotFoundError:
        st.warning("style.css not found.")


load_css()


# ============================================================
# DATABASE
# ============================================================

create_table()


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI ATS")

    st.markdown("---")

    st.subheader("About")

    st.write(
        """
Analyze resumes using an AI-powered ATS.

### Tech Stack

• LangGraph

• LangChain

• Google Gemini

• HuggingFace

• ChromaDB

• Streamlit
"""
    )

    st.markdown("---")

    st.metric("Version", "1.0")

    st.metric("LLM", "Google Gemini")

    st.metric("Embeddings", "BGE Small")

    st.markdown("---")

    st.success("AI Engineer Portfolio Project")


# ============================================================
# HEADER
# ============================================================

render_header()


# ============================================================
# UPLOAD SECTION
# ============================================================

col1, col2 = st.columns([1, 2])


with col1:

    uploaded_resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"],
    )


with col2:

    job_description = st.text_area(
        "💼 Job Description",
        height=350,
        placeholder="Paste Job Description Here...",
    )


st.divider()


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True,
):

    if uploaded_resume is None:
        st.error("Please upload your resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a Job Description.")
        st.stop()

    try:

        with st.spinner(
            "🤖 AI is analyzing your resume..."
        ):

            # ----------------------------------------
            # Save uploaded PDF temporarily
            # ----------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as tmp:

                tmp.write(uploaded_resume.getvalue())
                temp_pdf_path = tmp.name

            # ----------------------------------------
            # Extract resume text
            # ----------------------------------------

            resume_text = PDFLoader.extract_text(
                temp_pdf_path
            )

            # ----------------------------------------
            # Run ATS analysis
            # ----------------------------------------

            st.session_state.result = analyze_resume(
                resume_text,
                job_description,
            )

        st.success("✅ Analysis Completed!")

    except Exception as e:

        st.error("❌ Analysis failed.")

        st.exception(e)

        st.stop()


# ============================================================
# DISPLAY RESULT
# ============================================================

if st.session_state.result is not None:

    result = st.session_state.result

    st.divider()

    # ========================================================
    # ATS SCORE
    # ========================================================

    st.header("🎯 ATS Score")

    score_card(
        result.get("overall_score", 0),
        result.get(
            "recommendation",
            "No Recommendation"
        ),
    )

    st.progress(
        min(
            max(
                result.get("overall_score", 0),
                0
            ),
            100
        ) / 100
    )

    st.divider()


    # ========================================================
    # CANDIDATE SUMMARY
    # ========================================================

    st.header("👤 Candidate Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Candidate",
        result.get(
            "candidate_name",
            "Unknown"
        ),
    )

    c2.metric(
        "Experience",
        result.get(
            "resume_experience",
            "N/A"
        ),
    )

    c3.metric(
        "Education",
        result.get(
            "resume_education",
            "N/A"
        ),
    )

    st.divider()


    # ========================================================
    # ATS ANALYTICS
    # ========================================================

    st.header("📊 ATS Analytics")

    left, right = st.columns(2)

    with left:

        ats_gauge(
            result.get(
                "overall_score",
                0
            )
        )

    with right:

        skill_pie_chart(
            result.get(
                "matched_skills",
                []
            ),
            result.get(
                "missing_skills",
                []
            ),
        )

    st.divider()

    score_bar_chart(result)

    st.divider()


    # ========================================================
    # RESUME QUALITY
    # ========================================================

    st.header("📄 Resume Quality")

    resume_quality = result.get(
        "resume_quality_score",
        0
    )

    st.progress(
        min(max(resume_quality, 0), 100) / 100
    )

    st.metric(
        "Resume Quality",
        f"{resume_quality}%",
    )

    st.divider()


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    st.header("📊 Score Breakdown")

    a, b, c, d, e = st.columns(5)

    a.metric(
        "Skills",
        f"{result.get('skill_score', 0)}%"
    )

    b.metric(
        "Experience",
        f"{result.get('experience_score', 0)}%"
    )

    c.metric(
        "Education",
        f"{result.get('education_score', 0)}%"
    )

    d.metric(
        "Keywords",
        f"{result.get('keyword_score', 0)}%"
    )

    e.metric(
        "Resume",
        f"{result.get('resume_quality_score', 0)}%"
    )

    st.divider()


    # ========================================================
    # STRENGTHS & WEAKNESSES
    # ========================================================

    st.header("⭐ Candidate Evaluation")

    left, right = st.columns(2)

    with left:

        st.subheader("Strengths")

        strengths = result.get(
            "strengths",
            []
        )

        if strengths:

            for item in strengths:
                st.success(item)

        else:
            st.info("No strengths identified.")


    with right:

        st.subheader("Weaknesses")

        weaknesses = result.get(
            "weaknesses",
            []
        )

        if weaknesses:

            for item in weaknesses:
                st.error(item)

        else:
            st.info("No weaknesses identified.")


    st.divider()


    # ========================================================
    # STATISTICS
    # ========================================================

    stats_card(result)

    st.divider()


    # ========================================================
    # SKILLS
    # ========================================================

    skill_cards(
        result.get(
            "matched_skills",
            []
        ),
        result.get(
            "missing_skills",
            []
        ),
    )

    st.divider()


    # ========================================================
    # AI FEEDBACK
    # ========================================================

    feedback_card(
        result.get(
            "feedback",
            ""
        )
    )

    st.divider()


    # ========================================================
    # INTERVIEW QUESTIONS
    # ========================================================

    interview_card(
        result.get(
            "interview_questions",
            []
        )
    )

    st.divider()


    # ========================================================
    # PDF REPORT
    # ========================================================

    st.header("📄 ATS Report")

    pdf_file = "ATS_Report.pdf"

    try:

        generate_report(
            result,
            pdf_file
        )

        with open(
            pdf_file,
            "rb"
        ) as file:

            pdf_data = file.read()

        st.download_button(
            label="📥 Download ATS Report",
            data=pdf_data,
            file_name="ATS_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as e:

        st.error(
            f"Unable to generate PDF report: {e}"
        )


    # ========================================================
    # DEVELOPER MODE
    # ========================================================

    with st.expander("🔧 Developer Mode"):

        st.json(result)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Built with LangGraph, LangChain, Google Gemini, "
    "HuggingFace, ChromaDB and Streamlit."
)