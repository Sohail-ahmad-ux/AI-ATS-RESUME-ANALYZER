import streamlit as st


def interview_card(questions):

    st.markdown("## 🎯 Interview Questions")

    if isinstance(questions, str):

        st.markdown(questions)

        return

    for i, q in enumerate(questions, start=1):

        with st.expander(f"Question {i}"):

            st.write(q)