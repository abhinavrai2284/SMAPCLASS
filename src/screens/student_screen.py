import streamlit as st
import pandas as pd
from datetime import datetime
import time
from PIL import Image
import numpy as np

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
)
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def render_today_attendance_card(item):
    is_present = item['is_present']
    status_bg = "#ecfdf5" if is_present else "#fef2f2"
    status_color = "#047857" if is_present else "#b91c1c"
    status_border = "#a7f3d0" if is_present else "#fecaca"
    status_text = "âœ… PRESENT" if is_present else "âŒ ABSENT"

    html = f"""
    <div style="background: white; border: 1px solid #e2e8f0; border-left: 6px solid {'#10b981' if is_present else '#ef4444'}; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
        <div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #1e293b;">{item['subject_name']}</div>
            <div style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                <span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: 600; color: #475569;">Code: {item['subject_code']}</span>
                &nbsp;â€¢&nbsp; Section: <b>{item['section']}</b>
                &nbsp;â€¢&nbsp; ðŸ•’ Time: <b>{item['time']}</b>
            </div>
        </div>
        <div>
            <span style="background: {status_bg}; color: {status_color}; border: 1px solid {status_border}; padding: 7px 16px; border-radius: 25px; font-weight: 700; font-size: 0.95rem; display: inline-block;">
                {status_text}
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # Header and logout bar
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']} ðŸ‘‹")
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace", icon=":material/logout:"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    # Load student data
    with st.spinner('Loading attendance records...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # Date calculations
    today_dt = datetime.now()
    today_str = today_dt.strftime("%Y-%m-%d")
    today_display = today_dt.strftime("%A, %d %B %Y")

    today_logs = []
    all_logs_formatted = []
    stats_map = {}

    for log in logs:
        sid = log.get('subject_id')
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1
        is_present = bool(log.get('is_present', False))
        if is_present:
            stats_map[sid]['attended'] += 1

        ts = log.get('timestamp', '')
        formatted_date = 'N/A'
        formatted_time = 'N/A'
        is_today = False

        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                formatted_date = dt.strftime("%Y-%m-%d")
                formatted_time = dt.strftime("%I:%M %p")
                if dt.date() == today_dt.date() or ts.startswith(today_str):
                    is_today = True
            except Exception:
                if ts.startswith(today_str):
                    is_today = True
                formatted_date = ts[:10]
                formatted_time = ts[11:16] if len(ts) >= 16 else ts

        sub_info = log.get('subjects') or {}
        item = {
            'subject_name': sub_info.get('name', 'Unknown Subject'),
            'subject_code': sub_info.get('subject_code', '-'),
            'section': sub_info.get('section', '-'),
            'date': formatted_date,
            'time': formatted_time,
            'is_present': is_present,
            'timestamp': ts,
        }

        all_logs_formatted.append(item)
        if is_today:
            today_logs.append(item)

    # Overview Metrics Row
    total_classes = len(logs)
    total_attended = sum(1 for l in logs if l.get('is_present'))
    overall_pct = round((total_attended / total_classes * 100), 1) if total_classes > 0 else 0
    today_present = sum(1 for l in today_logs if l['is_present'])
    today_absent = sum(1 for l in today_logs if not l['is_present'])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="ðŸ“… Today", value=today_dt.strftime("%d %b %Y"))
    with m2:
        st.metric(label="âœ… Today's Present", value=f"{today_present} Class{'es' if today_present != 1 else ''}")
    with m3:
        st.metric(label="âŒ Today's Absent", value=f"{today_absent} Class{'es' if today_absent != 1 else ''}")
    with m4:
        st.metric(label="ðŸ“Š Overall Rate", value=f"{overall_pct}%")

    st.divider()

    # Dashboard Tabs
    tab_today, tab_subjects, tab_history = st.tabs([
        "ðŸ“‹ Today's Attendance (à¤†à¤œ à¤•à¥€ à¤¹à¤¾à¤œà¤¼à¤¿à¤°à¥€)",
        "ðŸ“š Enrolled Subjects (à¤¦à¤¾à¤–à¤¿à¤² à¤µà¤¿à¤·à¤¯)",
        "ðŸ“œ Full History (à¤ªà¥‚à¤°à¤¾ à¤°à¤¿à¤•à¥‰à¤°à¥à¤¡)",
    ])

    # TAB 1: TODAY'S ATTENDANCE LIST
    with tab_today:
        st.subheader(f"Today's Attendance List ({today_display})")

        if today_logs:
            st.caption(f"Showing {len(today_logs)} attendance record(s) recorded for today:")
            for item in today_logs:
                render_today_attendance_card(item)

            # Also provide a quick summary dataframe view option
            with st.expander("ðŸ“Š View as Table"):
                df_today = pd.DataFrame([
                    {
                        "Subject": item['subject_name'],
                        "Subject Code": item['subject_code'],
                        "Section": item['section'],
                        "Time": item['time'],
                        "Status": "âœ… Present" if item['is_present'] else "âŒ Absent",
                    }
                    for item in today_logs
                ])
                st.dataframe(df_today, hide_index=True, width='stretch')
        else:
            st.info(f"â„¹ï¸ **No attendance marked for today yet ({today_display}).**\n\nWhen your teacher takes attendance in class, your status (**Present** / **Absent**) will appear here automatically.")

    # TAB 2: ENROLLED SUBJECTS
    with tab_subjects:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader('Your Enrolled Subjects')
        with c2:
            if st.button('Enroll in Subject', type='primary', width='stretch'):
                enroll_dialog()

        if subjects:
            cols = st.columns(2)
            for i, sub_node in enumerate(subjects):
                sub = sub_node['subjects']
                sid = sub['subject_id']
                stats = stats_map.get(sid, {"total": 0, "attended": 0})

                def make_unenroll_callback(s_id=sid, s_name=sub['name']):
                    def unenroll_button():
                        if st.button("Unenroll from this course", type='tertiary', width='stretch', icon=':material/delete_forever:', key=f"unenroll_{s_id}"):
                            unenroll_student_to_subject(student_id, s_id)
                            st.toast(f'Unenrolled from {s_name} successfully!')
                            st.rerun()
                    return unenroll_button

                with cols[i % 2]:
                    subject_card(
                        name=sub['name'],
                        code=sub['subject_code'],
                        section=sub['section'],
                        stats=[
                            ('ðŸ“…', 'Total', stats['total']),
                            ('âœ…', 'Attended', stats['attended']),
                        ],
                        footer_callback=make_unenroll_callback(sid, sub['name']),
                    )
        else:
            st.info("You haven't enrolled in any subjects yet. Click **'Enroll in Subject'** above to join your classes.")

    # TAB 3: FULL HISTORY
    with tab_history:
        st.subheader("Complete Attendance History")
        if all_logs_formatted:
            df_history = pd.DataFrame([
                {
                    "Date": item['date'],
                    "Time": item['time'],
                    "Subject": item['subject_name'],
                    "Subject Code": item['subject_code'],
                    "Section": item['section'],
                    "Status": "âœ… Present" if item['is_present'] else "âŒ Absent",
                }
                for item in sorted(all_logs_formatted, key=lambda x: x['timestamp'], reverse=True)
            ])
            st.dataframe(df_history, hide_index=True, width='stretch')
        else:
            st.info("No attendance history found.")

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()

    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img_rgb = Image.open(photo_source).convert('RGB')

        with st.spinner('AI is scanning..'):
            encodings = get_face_embeddings(img_rgb)
            num_faces = len(encodings)

            if num_faces == 0:
                st.warning('âš ï¸ Face not detected! Please ensure proper lighting and face the camera directly.')
            elif num_faces > 1:
                st.warning('âš ï¸ Multiple faces found! Please ensure only one person is in the frame.')
            else:
                detected, all_ids, _ = predict_attendance(img_rgb)

                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('ðŸ‘¤ Face not recognized! You might be a new student. Please register below.')
                    show_registration = True

    if show_registration and photo_source:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll for voice only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Akash.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img_rgb = Image.open(photo_source).convert('RGB')
                        encodings = get_face_embeddings(img_rgb)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldn't capture your facial features for registration. Please retake the photo.")
                else:
                    st.warning('Please enter your name!')

    footer_dashboard()