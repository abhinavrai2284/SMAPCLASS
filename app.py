import streamlit as st


from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.ui.base_layout import style_base_layout


def main():
    st.set_page_config(layout="centered")

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    style_base_layout()

    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()

        case "student":
            student_screen()

        case None:
            home_screen()

main()