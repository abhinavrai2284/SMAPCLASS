import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    if "student_data" not in st.session_state or not st.session_state.student_data:
        st.warning("Please log in as a student first to enroll.")
        if st.button("Close"):
            st.rerun()
        return

    student_id = st.session_state.student_data['student_id']

    clean_code = str(subject_code).strip()
    res = supabase.table('subjects').select('subject_id, name, subject_code').ilike('subject_code', clean_code).execute()
    if not res.data:
        res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', clean_code).execute()
    if not res.data:
        st.error('Subject Code not found!')
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.info("You're already enrolled!")
        if st.button('Got it!'):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"Would you like to enroll in **{subject['name']}**?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', width='stretch'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('Joined successfully!')
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
