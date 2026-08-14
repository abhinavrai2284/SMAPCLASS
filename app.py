
import streamlit as st

from src.database.config import supabase
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",
        layout="centered"
    )

    if supabase is None:
        st.error("⚠️ **Database Connection Error: Supabase credentials not found!**")
        st.info("""
        Please configure your Supabase credentials in Streamlit Cloud Secrets:
        1. Click on **Manage app** (in the bottom-right).
        2. Go to **Settings (⚙️) > Secrets**.
        3. Paste:
        ```toml
        SUPABASE_URL = "https://lddkomsesyexjwdtskfh.supabase.co"
        SUPABASE_KEY = "sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"
        ```
        4. Click **Save**.
        """)
        return

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()


    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
main()