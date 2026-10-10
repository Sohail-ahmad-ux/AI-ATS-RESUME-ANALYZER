from components.comparison import compare_candidates
from components.charts import (
    ats_gauge,
    skill_pie_chart,
    score_bar_chart,
)
import streamlit as st
import pandas as pd

from database.db import (
    get_candidates,
    search_candidate,
    delete_candidate,
    filter_candidates,
    sort_candidates,
    get_dashboard_stats
)

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Recruiter Dashboard",
    page_icon="📋",
    layout="wide"
)

# ======================================================
# Title
# ======================================================

st.title("📋 Recruiter Dashboard")
st.caption("Manage, search and compare all analyzed candidates.")

# ======================================================
# Dashboard Statistics
# ======================================================

stats = get_dashboard_stats()

st.divider()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "👥 Candidates",
    stats["total"]
)

c2.metric(
    "📊 Avg ATS",
    f"{stats['average']}%"
)

c3.metric(
    "🟢 Strong Fit",
    stats["strong"]
)

c4.metric(
    "🟡 Moderate",
    stats["moderate"]
)

c5.metric(
    "🔴 Weak",
    stats["weak"]
)

st.divider()
st.divider()

st.subheader("📊 ATS Analytics")

left, right = st.columns(2)

with left:

    ats_gauge(stats["average"])

with right:

    recommendation_data = {

        "Matched": stats["strong"],

        "Moderate": stats["moderate"],

        "Weak": stats["weak"]

    }

    skill_pie_chart(

        list(recommendation_data.keys()),

        list(recommendation_data.values())

    )
# ======================================================
# Search / Filter / Sort
# ======================================================

st.subheader("🔍 Candidate Search")

col1, col2, col3 = st.columns(3)

with col1:
    search = st.text_input(
        "Candidate Name",
        placeholder="Search by candidate name..."
    )

with col2:
    recommendation = st.selectbox(
        "Recommendation",
        [
            "All",
            "Strong Fit",
            "Moderate Fit",
            "Weak Fit"
        ]
    )

with col3:
    sort = st.selectbox(
        "Sort ATS Score",
        [
            "Highest",
            "Lowest"
        ]
    )

# ======================================================
# Fetch Candidates
# ======================================================

if search:
    rows = search_candidate(search)

elif recommendation != "All":
    rows = filter_candidates(recommendation)

elif sort == "Lowest":
    rows = sort_candidates("ASC")

else:
    rows = sort_candidates("DESC")

# ======================================================
# Candidate Table
# ======================================================

columns = [
    "ID",
    "Candidate",
    "ATS Score",
    "Recommendation",
    "Matched Skills",
    "Missing Skills",
    "Feedback",
    "Interview",
    "Created"
]

df = pd.DataFrame(rows, columns=columns)

st.subheader("📋 Candidate Records")

if df.empty:

    st.warning("No candidates found.")

else:

    for _, row in df.iterrows():

        with st.expander(
            f"👤 {row['Candidate']} | ATS: {row['ATS Score']}%"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "ATS Score",
                    f"{row['ATS Score']}%"
                )

                st.metric(
                    "Recommendation",
                    row["Recommendation"]
                )

            with col2:

                st.write("### ✅ Matched Skills")
                st.write(row["Matched Skills"])

                st.write("### ❌ Missing Skills")
                st.write(row["Missing Skills"])

            st.divider()

            st.subheader("AI Feedback")
            st.info(row["Feedback"])

            st.divider()

            st.subheader("Interview Questions")
            st.write(row["Interview"])

            st.divider()

            if st.button(
                "🗑 Delete Candidate",
                key=f"delete_{row['ID']}"
            ):

                delete_candidate(row["ID"])

                st.success("Candidate deleted successfully.")

                st.rerun()

# ==========================================
# Candidate Comparison
# ==========================================

st.divider()

compare_candidates(df)                