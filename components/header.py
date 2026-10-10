import streamlit as st

def render_header():
    st.markdown("""
    <h1 class="title">🤖 AI ATS Resume Analyzer</h1>

    <p class="subtitle">
        Upload your resume and compare it against any Job Description using AI.
    </p>
    """, unsafe_allow_html=True)