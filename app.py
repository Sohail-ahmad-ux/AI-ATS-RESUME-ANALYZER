
import streamlit as st
import tempfile
import os
import io

# Charts
import matplotlib.pyplot as plt

# PDF Report
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from graph import graph
from utils.pdf_loader import PDFLoader


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .ats-header {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        margin-bottom: 25px;
    }

    .ats-header h1 {
        margin-bottom: 5px;
    }

    .ats-header p {
        color: #d1d5db;
        margin-top: 0;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280;
    }

    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: #111827;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .skill {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        background: #e0f2fe;
        color: #075985;
        font-size: 14px;
    }

    .missing-skill {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        background: #fee2e2;
        color: #991b1b;
        font-size: 14px;
    }

    .sidebar-box {
        padding: 15px;
        border-radius: 10px;
        background: #f8fafc;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_score(result, key, default=0):
    """Safely return a numeric score."""
    value = result.get(key, default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def get_list(result, key):
    """Safely return a list."""
    value = result.get(key, [])

    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [str(value)]


def score_color(score):
    """Return a simple status based on ATS score."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Moderate"
    else:
        return "Low"


# ============================================================
# ATS GAUGE
# ============================================================

def create_ats_gauge(score):
    fig, ax = plt.subplots(figsize=(6, 3))

    score = max(0, min(100, score))

    ax.barh(
        [0],
        [100],
        height=0.35,
        alpha=0.15,
    )

    ax.barh(
        [0],
        [score],
        height=0.35,
    )

    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("ATS Score")

    ax.text(
        score,
        0,
        f"  {score:.1f}%",
        va="center",
        fontsize=16,
        fontweight="bold",
    )

    ax.set_title(
        "ATS Score",
        fontsize=18,
        fontweight="bold",
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# SKILL CHART
# ============================================================

def create_skill_chart(matched, missing):
    matched_count = len(matched)
    missing_count = len(missing)

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(
        ["Matched Skills", "Missing Skills"],
        [matched_count, missing_count],
    )

    ax.set_ylabel("Number of Skills")
    ax.set_title(
        "Skills Analysis",
        fontsize=16,
        fontweight="bold",
    )

    for i, value in enumerate([matched_count, missing_count]):
        ax.text(
            i,
            value,
            str(value),
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# SCORE BREAKDOWN CHART
# ============================================================

def create_score_breakdown(result):

    categories = [
        "Skills",
        "Experience",
        "Education",
        "Keywords",
        "Resume Quality",
    ]

    values = [
        get_score(result, "skill_score"),
        get_score(result, "experience_score"),
        get_score(result, "education_score"),
        get_score(result, "keyword_score"),
        get_score(result, "resume_quality_score"),
    ]

    fig, ax = plt.subplots(figsize=(10, 4))

    bars = ax.bar(categories, values)

    ax.set_ylim(0, 100)
    ax.set_ylabel("Score (%)")
    ax.set_title(
        "ATS Score Breakdown",
        fontsize=16,
        fontweight="bold",
    )

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 2,
            f"{value:.0f}%",
            ha="center",
            fontweight="bold",
        )

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# PDF REPORT
# ============================================================

def generate_pdf_report(result):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=15,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
    )

    story = []

    candidate = result.get(
        "candidate_name",
        "Unknown Candidate",
    )

    overall = get_score(
        result,
        "overall_score",
    )

    recommendation = result.get(
        "recommendation",
        "N/A",
    )

    # Title
    story.append(
        Paragraph(
            "AI ATS Resume Analysis Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Candidate:</b> {candidate}",
            normal_style,
        )
    )

    story.append(Spacer(1, 10))

    # ATS Score
    story.append(
        Paragraph(
            "ATS Score",
            heading_style,
        )
    )

    score_table = Table(
        [
            [
                Paragraph(
                    f"<b>{overall:.1f}%</b>",
                    normal_style,
                ),
                Paragraph(
                    f"<b>{recommendation}</b>",
                    normal_style,
                ),
            ]
        ],
        colWidths=[200, 250],
    )

    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                ("BOX", (0, 0), (-1, -1), 1, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )

    story.append(score_table)

    # Candidate information
    story.append(
        Paragraph(
            "Candidate Information",
            heading_style,
        )
    )

    candidate_data = [
        [
            "Candidate",
            candidate,
        ],
        [
            "Experience",
            str(result.get("resume_experience", "N/A")),
        ],
        [
            "Education",
            str(result.get("resume_education", "N/A")),
        ],
        [
            "Recommendation",
            recommendation,
        ],
    ]

    table = Table(
        candidate_data,
        colWidths=[150, 300],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(table)

    # Score breakdown
    story.append(
        Paragraph(
            "Score Breakdown",
            heading_style,
        )
    )

    score_data = [
        ["Category", "Score"],
        [
            "Skills",
            f"{get_score(result, 'skill_score'):.1f}%",
        ],
        [
            "Experience",
            f"{get_score(result, 'experience_score'):.1f}%",
        ],
        [
            "Education",
            f"{get_score(result, 'education_score'):.1f}%",
        ],
        [
            "Keywords",
            f"{get_score(result, 'keyword_score'):.1f}%",
        ],
        [
            "Resume Quality",
            f"{get_score(result, 'resume_quality_score'):.1f}%",
        ],
    ]

    table = Table(
        score_data,
        colWidths=[250, 200],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(table)

    # Skills
    matched = get_list(result, "matched_skills")
    missing = get_list(result, "missing_skills")

    story.append(
        Paragraph(
            "Skills Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Matched Skills</b>",
            normal_style,
        )
    )

    for skill in matched:
        story.append(
            Paragraph(
                f"• {skill}",
                normal_style,
            )
        )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            normal_style,
        )
    )

    for skill in missing:
        story.append(
            Paragraph(
                f"• {skill}",
                normal_style,
            )
        )

    # Strengths
    strengths = get_list(result, "strengths")

    story.append(
        Paragraph(
            "Strengths",
            heading_style,
        )
    )

    for item in strengths:
        story.append(
            Paragraph(
                f"• {item}",
                normal_style,
            )
        )

    # Weaknesses
    weaknesses = get_list(result, "weaknesses")

    story.append(
        Paragraph(
            "Areas for Improvement",
            heading_style,
        )
    )

    for item in weaknesses:
        story.append(
            Paragraph(
                f"• {item}",
                normal_style,
            )
        )

    # Feedback
    feedback = result.get(
        "feedback",
        "",
    )

    if feedback:
        story.append(
            Paragraph(
                "AI Resume Feedback",
                heading_style,
            )
        )

        for paragraph in str(feedback).split("\n"):
            paragraph = paragraph.strip()

            if paragraph:
                story.append(
                    Paragraph(
                        paragraph,
                        normal_style,
                    )
                )

                story.append(
                    Spacer(1, 5)
                )

    # Interview Questions
    questions = get_list(
        result,
        "interview_questions",
    )

    if questions:
        story.append(
            Paragraph(
                "Interview Questions",
                heading_style,
            )
        )

        for index, question in enumerate(
            questions,
            start=1,
        ):
            story.append(
                Paragraph(
                    f"{index}. {question}",
                    normal_style,
                )
            )

            story.append(
                Spacer(1, 5)
            )

    doc.build(story)

    buffer.seek(0)

    return buffer


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-box">
        <h2>📄 AI ATS</h2>
        <p>AI-powered Resume Screening System</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Technology")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• LangGraph")
    st.write("• LangChain")
    st.write("• Groq")
    st.write("• HuggingFace")
    st.write("• ChromaDB")

    st.divider()

    st.markdown("### System")

    st.write("ATS Resume Analyzer")
    st.write("AI Candidate Evaluation")
    st.write("Resume–Job Matching")

    st.divider()

    st.caption("AI ATS Resume Analyzer")
    st.caption("Version 1.0")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="ats-header">
        <h1>📄 AI Resume ATS Analyzer</h1>
        <p>
        Analyze a resume against a job description using an AI-powered
        recruitment pipeline.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT SECTION
# ============================================================

input_col1, input_col2 = st.columns(
    [1, 2]
)

with input_col1:

    st.subheader("📄 Resume")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
    )

with input_col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )


# ============================================================
# ANALYZE
# ============================================================

if st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True,
):

    if uploaded_file is None:
        st.error(
            "Please upload a resume."
        )
        st.stop()

    if not job_description.strip():
        st.error(
            "Please enter a job description."
        )
        st.stop()

    try:

        with st.spinner(
            "🤖 AI is analyzing the resume..."
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as tmp:

                tmp.write(
                    uploaded_file.read()
                )

                pdf_path = tmp.name

            try:

                resume_text = (
                    PDFLoader.extract_text(
                        pdf_path
                    )
                )

            finally:

                if os.path.exists(pdf_path):
                    os.remove(pdf_path)

            state = {
                "resume_text": resume_text,
                "job_description": job_description,
            }

            result = graph.invoke(state)

            st.session_state.result = result
            st.session_state.resume_text = resume_text

        st.success(
            "✅ Analysis completed successfully!"
        )

    except Exception as e:

        st.error(
            f"Analysis failed: {str(e)}"
        )

        st.exception(e)
        st.stop()


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result:

    result = st.session_state.result

    # --------------------------------------------------------
    # BASIC DATA
    # --------------------------------------------------------

    candidate_name = result.get(
        "candidate_name",
        "Unknown Candidate",
    )

    overall_score = get_score(
        result,
        "overall_score",
    )

    match_score = get_score(
        result,
        "match_score",
        overall_score,
    )

    recommendation = result.get(
        "recommendation",
        "N/A",
    )

    matched_skills = get_list(
        result,
        "matched_skills",
    )

    missing_skills = get_list(
        result,
        "missing_skills",
    )

    strengths = get_list(
        result,
        "strengths",
    )

    weaknesses = get_list(
        result,
        "weaknesses",
    )

    # --------------------------------------------------------
    # CANDIDATE HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">👤 Candidate Evaluation</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Candidate",
        candidate_name,
    )

    c2.metric(
        "Skill Match",
        f"{match_score:.1f}%",
    )

    c3.metric(
        "ATS Score",
        f"{overall_score:.1f}%",
    )

    c4.metric(
        "Status",
        score_color(overall_score),
    )

    st.progress(
        max(0.0, min(1.0, overall_score / 100))
    )

    st.info(
        f"Recommendation: {recommendation}"
    )

    st.divider()

    # --------------------------------------------------------
    # ATS ANALYTICS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 ATS Analytics</div>',
        unsafe_allow_html=True,
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.subheader("ATS Score")

        create_ats_gauge(
            overall_score
        )

    with chart_col2:

        st.subheader("Skills")

        create_skill_chart(
            matched_skills,
            missing_skills,
        )

    st.divider()

    # --------------------------------------------------------
    # SCORE BREAKDOWN
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📈 Score Breakdown</div>',
        unsafe_allow_html=True,
    )

    create_score_breakdown(
        result
    )

    score_cols = st.columns(5)

    score_fields = [
        ("Skills", "skill_score"),
        ("Experience", "experience_score"),
        ("Education", "education_score"),
        ("Keywords", "keyword_score"),
        ("Resume Quality", "resume_quality_score"),
    ]

    for column, (label, key) in zip(
        score_cols,
        score_fields,
    ):

        with column:

            score = get_score(
                result,
                key,
            )

            st.metric(
                label,
                f"{score:.1f}%",
            )

    st.divider()

    # --------------------------------------------------------
    # CANDIDATE INFORMATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Candidate Information</div>',
        unsafe_allow_html=True,
    )

    info1, info2 = st.columns(2)

    with info1:

        st.write(
            "**Candidate:**",
            candidate_name,
        )

        st.write(
            "**Experience:**",
            result.get(
                "resume_experience",
                "N/A",
            ),
        )

    with info2:

        st.write(
            "**Education:**",
            result.get(
                "resume_education",
                "N/A",
            ),
        )

        st.write(
            "**Recommendation:**",
            recommendation,
        )

    st.divider()

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🧠 Skills Analysis</div>',
        unsafe_allow_html=True,
    )

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:

        st.subheader(
            f"✅ Matched Skills ({len(matched_skills)})"
        )

        if matched_skills:

            for skill in matched_skills:

                st.markdown(
                    f'<span class="skill">{skill}</span>',
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No matched skills found."
            )

    with skill_col2:

        st.subheader(
            f"❌ Missing Skills ({len(missing_skills)})"
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f'<span class="missing-skill">{skill}</span>',
                    unsafe_allow_html=True,
                )

        else:

            st.success(
                "No missing skills found."
            )

    st.divider()

    # --------------------------------------------------------
    # STRENGTHS / WEAKNESSES
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">⭐ Candidate Evaluation</div>',
        unsafe_allow_html=True,
    )

    evaluation_col1, evaluation_col2 = st.columns(2)

    with evaluation_col1:

        st.subheader("💪 Strengths")

        if strengths:

            for item in strengths:
                st.success(item)

        else:

            st.info(
                "No strengths provided."
            )

    with evaluation_col2:

        st.subheader("⚠️ Weaknesses")

        if weaknesses:

            for item in weaknesses:
                st.warning(item)

        else:

            st.info(
                "No weaknesses provided."
            )

    st.divider()

    # --------------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------------

    feedback = result.get(
        "feedback",
        "",
    )

    if feedback:

        st.markdown(
            '<div class="section-title">🤖 AI Resume Feedback</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            feedback
        )

        st.divider()

    # --------------------------------------------------------
    # INTERVIEW QUESTIONS
    # --------------------------------------------------------

    interview_questions = get_list(
        result,
        "interview_questions",
    )

    if interview_questions:

        st.markdown(
            '<div class="section-title">🎯 Interview Questions</div>',
            unsafe_allow_html=True,
        )

        for index, question in enumerate(
            interview_questions,
            start=1,
        ):

            st.write(
                f"**{index}.** {question}"
            )

        st.divider()

    # --------------------------------------------------------
    # PDF REPORT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📄 ATS Report</div>',
        unsafe_allow_html=True,
    )

    pdf_buffer = generate_pdf_report(
        result
    )

    st.download_button(
        label="📥 Download ATS Report PDF",
        data=pdf_buffer,
        file_name="ATS_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.success(
        "ATS report is ready."
    )

    st.divider()

    # --------------------------------------------------------
    # DEVELOPER MODE
    # --------------------------------------------------------

    with st.expander(
        "🛠️ Developer Mode"
    ):

        st.json(
            result
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "---"
)

st.caption(
    "AI ATS Resume Analyzer • Built with Python, Streamlit, LangGraph, LangChain and AI"
)
