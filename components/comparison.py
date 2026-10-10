import streamlit as st
import pandas as pd


def compare_candidates(df):

    st.header("⚖️ Candidate Comparison")

    if len(df) < 2:
        st.info("At least two candidates are required for comparison.")
        return

    names = df["Candidate"].tolist()

    col1, col2 = st.columns(2)

    with col1:
        candidate1 = st.selectbox(
            "Candidate 1",
            names,
            key="candidate_1"
        )

    with col2:
        candidate2 = st.selectbox(
            "Candidate 2",
            names,
            index=1 if len(names) > 1 else 0,
            key="candidate_2"
        )

    if candidate1 == candidate2:
        st.warning("Please choose two different candidates.")
        return

    row1 = df[df["Candidate"] == candidate1].iloc[0]
    row2 = df[df["Candidate"] == candidate2].iloc[0]

    comparison = pd.DataFrame({

        "Metric": [
            "ATS Score",
            "Recommendation",
            "Matched Skills",
            "Missing Skills"
        ],

        candidate1: [
            row1["ATS Score"],
            row1["Recommendation"],
            row1["Matched Skills"],
            row1["Missing Skills"]
        ],

        candidate2: [
            row2["ATS Score"],
            row2["Recommendation"],
            row2["Matched Skills"],
            row2["Missing Skills"]
        ]

    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )