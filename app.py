import streamlit as st

from src.database.config import supabase
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='SMAPCLASS - AI Classroom Attendance & Intelligence',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    if supabase is None:
        st.error("⚠️ **Database Connection Error: Supabase credentials not found!**")
        st.info("""
        Please configure your Supabase credentials in Streamlit Cloud Secrets / .env:
        ```toml
        SUPABASE_URL = "https://lddkomsesyexjwdtskfh.supabase.co"
        SUPABASE_KEY = "sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"
        ```
        """)
        return

    # Check query param for direct navigation from landing page iframe
    role_param = st.query_params.get('role')
    if role_param in ['teacher', 'student']:
        st.session_state['login_type'] = role_param
    elif 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # Routing
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case _:
            home_screen()

    # Join Code Auto-Enrollment
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.get('login_type') != 'student':
            st.session_state['login_type'] = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == '__main__':
    main()