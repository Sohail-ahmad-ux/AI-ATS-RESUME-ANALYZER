import streamlit as st


def stats_card(result):

    st.markdown("## 📄 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Matched Skills",
            len(result["matched_skills"])
        )

        st.metric(
            "Missing Skills",
            len(result["missing_skills"])
        )

    with col2:

        st.metric(
            "Resume Skills",
            len(result["resume_skills"])
        )

        st.metric(
            "Required Skills",
            len(result["required_skills"])
        )