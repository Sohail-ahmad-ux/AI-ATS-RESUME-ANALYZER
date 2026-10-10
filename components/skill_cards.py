import streamlit as st


def skill_cards(matched, missing):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matched Skills")

        if matched:
            for skill in matched:
                st.success(skill)
        else:
            st.info("No matched skills.")

    with col2:
        st.markdown("### ❌ Missing Skills")

        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.success("No missing skills.")