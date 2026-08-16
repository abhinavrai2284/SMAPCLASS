import streamlit as st

from src.database.config import supabase
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog


def main():
    st.set_page_config(
        page_title="SMAPCLASS - Next-Gen AI Biometric Classroom Attendance",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Supabase Connection Guard
    if supabase is None:
        st.error("⚠️ **Database Connection Error: Supabase credentials not found or invalid!**")
        st.info("""
        **How to configure Supabase:**
        1. For local development, create a `.env` file in the project root:
        ```env
        SUPABASE_URL="https://your-supabase-url.supabase.co"
        SUPABASE_KEY="your-supabase-anon-or-service-key"
        ```
        2. For **Streamlit Cloud Deployment**, configure **Settings (⚙️) > Secrets**:
        ```toml
        SUPABASE_URL = "https://your-supabase-url.supabase.co"
        SUPABASE_KEY = "your-supabase-anon-or-service-key"
        ```
        """)
        return

    # Handle URL query parameters (?role=teacher, ?role=student, ?join-code=XYZ)
    role_param = st.query_params.get("role")
    join_code = st.query_params.get("join-code")

    if "login_type" not in st.session_state:
        if role_param in ["teacher", "student"]:
            st.session_state["login_type"] = role_param
        elif join_code:
            st.session_state["login_type"] = "student"
        else:
            st.session_state["login_type"] = None

    # Render Current Active Screen
    match st.session_state.get("login_type"):
        case "teacher":
            teacher_screen()

        case "student":
            student_screen()

        case _:
            home_screen()

    # Handle Auto Enroll Dialog Trigger for Students
    if join_code:
        if st.session_state.get("login_type") != "student":
            st.session_state["login_type"] = "student"
            st.rerun()
        if st.session_state.get("is_logged_in") and st.session_state.get("user_role") == "student":
            auto_enroll_dialog(join_code)


if __name__ == "__main__":
    main()