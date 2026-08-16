import streamlit as st


@st.dialog("Share Class Details")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "smapclassapp.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(f"### {subject_name}")

    st.markdown("#### Subject Code")
    st.code(subject_code, language="text")

    st.markdown("#### Direct Join Link")
    st.code(join_url, language="text")

    st.info("Copy this code or link to share with students on WhatsApp or Email.")