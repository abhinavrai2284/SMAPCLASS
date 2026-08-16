import io
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image
import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier, _parse_embedding
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
    create_attendance,
    parse_student_details,
)
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def mark_student_attendance_for_today(student_id, subjects=None):
    """Automatically records is_present=True attendance for the student's enrolled courses today."""
    if not subjects:
        subjects = get_student_subjects(student_id)
    if not subjects:
        return 0

    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")
    existing_logs = get_student_attendance(student_id)
    already_marked_subjects = set(
        log['subject_id'] for log in existing_logs 
        if log.get('timestamp', '').startswith(today_str) and log.get('is_present')
    )

    new_logs = []
    for sub_node in subjects:
        sub = sub_node.get('subjects')
        if sub and sub['subject_id'] not in already_marked_subjects:
            new_logs.append({
                'student_id': student_id,
                'subject_id': sub['subject_id'],
                'timestamp': now_iso,
                'is_present': True
            })

    if new_logs:
        create_attendance(new_logs)
        return len(new_logs)
    return 0


def render_today_attendance_card(item):
    is_present = item['is_present']
    status_bg = "#ecfdf5" if is_present else "#fef2f2"
    status_color = "#047857" if is_present else "#b91c1c"
    status_border = "#a7f3d0" if is_present else "#fecaca"
    status_text = "✅ PRESENT" if is_present else "❌ ABSENT"

    html = f"""
    <div style="background: white; border: 1px solid #e2e8f0; border-left: 6px solid {'#10b981' if is_present else '#ef4444'}; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
        <div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #1e293b;">{item['subject_name']}</div>
            <div style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                <span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: 600; color: #475569;">Code: {item['subject_code']}</span>
                &nbsp;•&nbsp; Section: <b>{item['section']}</b>
                &nbsp;•&nbsp; 🕒 Time: <b>{item['time']}</b>
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
    parsed_info = parse_student_details(student_data)
    display_name = parsed_info['name']
    phone_num = parsed_info['phone_number']

    # Header and logout bar
    c1, c2 = st.columns([1.2, 1.8], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        sub_c1, sub_c2 = st.columns([2, 1], vertical_alignment='center')
        with sub_c1:
            st.markdown(f"<div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>Welcome, {display_name} 👋</div>", unsafe_allow_html=True)
            if phone_num and phone_num != "N/A":
                st.caption(f"📱 Registered Mobile: **{phone_num}**")
        with sub_c2:
            if st.button("🚪 Logout", type='secondary', key='loginbackbtn', use_container_width=True):
                st.session_state['is_logged_in'] = False
                if 'student_data' in st.session_state:
                    del st.session_state.student_data
                st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Load student data
    with st.spinner('Loading attendance records...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # Quick Self-Attendance Check-In Card
    checkin_c1, checkin_c2 = st.columns([2.5, 1.5], vertical_alignment="center")
    with checkin_c1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(88, 101, 242, 0.08) 0%, rgba(235, 69, 158, 0.08) 100%); border: 1px solid rgba(88, 101, 242, 0.2); border-radius: 14px; padding: 12px 18px;">
                <div style="font-weight: 700; color: #1e293b; font-size: 0.95rem;">⚡ Self Attendance Check-In</div>
                <div style="color: #64748b; font-size: 0.85rem;">Click check-in to confirm your presence for today's classes:</div>
            </div>
        """, unsafe_allow_html=True)
    with checkin_c2:
        if st.button("✅ Check In for Today", type="primary", use_container_width=True, key="btn_self_checkin"):
            marked = mark_student_attendance_for_today(student_id, subjects)
            if marked > 0:
                st.toast(f"✅ Marked present for {marked} subject(s) today!", icon="🎉")
                time.sleep(1)
                st.rerun()
            else:
                st.info("ℹ️ You are already marked present for all enrolled subjects today!")

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

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
        st.metric(label="📅 Today", value=today_dt.strftime("%d %b %Y"))
    with m2:
        st.metric(label="✅ Today's Present", value=f"{today_present} Class{'es' if today_present != 1 else ''}")
    with m3:
        st.metric(label="❌ Today's Absent", value=f"{today_absent} Class{'es' if today_absent != 1 else ''}")
    with m4:
        st.metric(
            label="📊 Overall Rate", 
            value=f"{overall_pct}%",
            delta="Eligible (>=75%)" if overall_pct >= 75.0 else "⚠️ Low Attendance (<75%)",
            delta_color="normal" if overall_pct >= 75.0 else "inverse"
        )

    if total_classes > 0 and overall_pct < 75.0:
        st.warning(f"⚠️ **Attendance Alert:** Your current overall attendance is **{overall_pct}%**, which is below the mandatory **75%** threshold. Please attend upcoming lectures regularly.")

    st.divider()

    # Dashboard Tabs
    tab_today, tab_subjects, tab_history = st.tabs([
        "📋 Today's Attendance",
        "📚 Enrolled Subjects",
        "📜 Full History",
    ])

    # TAB 1: TODAY'S ATTENDANCE LIST
    with tab_today:
        st.subheader(f"Today's Attendance List ({today_display})")

        if today_logs:
            st.caption(f"Showing {len(today_logs)} attendance record(s) recorded for today:")
            for item in today_logs:
                render_today_attendance_card(item)

            with st.expander("📊 View as Table"):
                df_today = pd.DataFrame([
                    {
                        "Subject": item['subject_name'],
                        "Subject Code": item['subject_code'],
                        "Section": item['section'],
                        "Time": item['time'],
                        "Status": "✅ Present" if item['is_present'] else "❌ Absent",
                    }
                    for item in today_logs
                ])
                st.dataframe(df_today, hide_index=True, use_container_width=True)
        else:
            st.info(f"ℹ️ **No attendance marked for today yet ({today_display}).**\n\nClick **'✅ Check In for Today'** above or have your teacher take attendance in class to mark your presence.")

    # TAB 2: ENROLLED SUBJECTS
    with tab_subjects:
        c1, c2 = st.columns([2, 1], vertical_alignment='center')
        with c1:
            st.subheader('Your Enrolled Subjects')
        with c2:
            if st.button('➕ Enroll in Subject', type='primary', use_container_width=True):
                enroll_dialog()

        if subjects:
            cols = st.columns(2)
            for i, sub_node in enumerate(subjects):
                sub = sub_node['subjects']
                sid = sub['subject_id']
                stats = stats_map.get(sid, {"total": 0, "attended": 0})
                sub_pct = round(stats['attended'] / stats['total'] * 100, 1) if stats['total'] > 0 else 100.0

                def make_unenroll_callback(s_id=sid, s_name=sub['name']):
                    def unenroll_button():
                        if st.button("🗑️ Unenroll", type='tertiary', use_container_width=True, key=f"unenroll_{s_id}"):
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
                            ('📅', 'Total', stats['total']),
                            ('✅', 'Attended', stats['attended']),
                            ('📊', 'Rate', f"{sub_pct}%"),
                        ],
                        footer_callback=make_unenroll_callback(sid, sub['name']),
                    )
        else:
            st.info("You haven't enrolled in any subjects yet. Click **'➕ Enroll in Subject'** above to join your classes.")

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
                    "Status": "✅ Present" if item['is_present'] else "❌ Absent",
                }
                for item in sorted(all_logs_formatted, key=lambda x: x['timestamp'], reverse=True)
            ])
            st.dataframe(df_history, hide_index=True, use_container_width=True)
        else:
            st.info("No attendance history found.")

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', use_container_width=True):
            st.session_state['login_type'] = None
            st.query_params.clear()
            st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    tab_login, tab_register = st.tabs([
        "👤 FaceID Login & Auto-Attendance (लॉगिन एवं हाज़िरी)",
        "📝 Register New Student (नया छात्र पंजीकरण)",
    ])

    # -------------------------------------------------------------------
    # TAB 1: FaceID Login & Auto Attendance
    # -------------------------------------------------------------------
    with tab_login:
        st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 1.5rem;">
                <h3 style="color: #1e293b; font-size: 1.3rem; margin-bottom: 0.3rem;">Student FaceID Login & Check-In</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1rem;">Take a snapshot facing the camera. Your identity will be verified, your attendance recorded for today's classes, and you'll be logged into your dashboard.</p>
        """, unsafe_allow_html=True)

        login_photo = st.camera_input("Position your face in the camera", key="student_camera_login")

        if login_photo is not None:
            photo_bytes = login_photo.getvalue()
            img_rgb = Image.open(io.BytesIO(photo_bytes)).convert('RGB')

            with st.spinner('🔍 AI is verifying face biometrics & logging attendance...'):
                encodings = get_face_embeddings(img_rgb)
                num_faces = len(encodings)

                if num_faces == 0:
                    st.warning('⚠️ Face not detected! Please ensure proper lighting and face the camera directly.')
                elif num_faces > 1:
                    st.warning('⚠️ Multiple faces detected! Please ensure only one student is in front of the camera.')
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

                            # Auto record attendance for today upon FaceID login
                            marked_count = mark_student_attendance_for_today(student_id)

                            if marked_count > 0:
                                st.toast(f"✅ Attendance recorded for {marked_count} subject(s) today!", icon="🎉")
                            st.toast(f"Welcome Back, {student.get('clean_name', student.get('name'))}! 👋")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info("👤 **Face not recognized!** You might be a new student. Please switch to the **'📝 Register New Student'** tab above to register your profile.")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # TAB 2: Register New Student (With Duplicate & Phone Number Support)
    # -------------------------------------------------------------------
    with tab_register:
        st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 1.5rem;">
                <h3 style="color: #1e293b; font-size: 1.3rem; margin-bottom: 0.3rem;">New Student Biometric Registration</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1.2rem;">Enter your full name, mobile number, and take a facial snapshot. <b>Note:</b> Each student can only register once.</p>
        """, unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            new_student_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma", key="reg_student_name")
        with col_f2:
            new_student_phone = st.text_input("Mobile / WhatsApp Number * (for SMS Alerts)", placeholder="e.g. 9876543210 or +919876543210", key="reg_student_phone")

        st.markdown("<div style='font-weight: 600; color: #1e293b; margin-top: 1rem; margin-bottom: 0.3rem;'>📸 Face Biometric Snapshot *</div>", unsafe_allow_html=True)
        reg_photo = st.camera_input("Capture facial snapshot for attendance", key="reg_camera_input")

        st.markdown("<div style='font-weight: 600; color: #1e293b; margin-top: 1.2rem; margin-bottom: 0.3rem;'>🎙️ Voice Signature (Optional)</div>", unsafe_allow_html=True)
        st.caption('Speak: "I am present in class" to enable Voice Attendance identification.')

        reg_audio = None
        try:
            reg_audio = st.audio_input("Record voice sample", key="reg_audio_input")
        except Exception:
            pass

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        if st.button("✨ Complete Biometric Registration", type="primary", use_container_width=True, key="btn_complete_registration"):
            if not new_student_name or not new_student_name.strip():
                st.error("❌ Please enter your **Full Name**.")
            elif not new_student_phone or not new_student_phone.strip():
                st.error("❌ Please enter your **Mobile / WhatsApp Number** for SMS attendance alerts.")
            elif reg_photo is None:
                st.error("❌ Please take a **Face Biometric Snapshot** using the camera above.")
            else:
                with st.spinner("🧠 Analyzing facial biometrics & checking for duplicate profiles..."):
                    photo_bytes = reg_photo.getvalue()
                    img_rgb = Image.open(io.BytesIO(photo_bytes)).convert('RGB')
                    encodings = get_face_embeddings(img_rgb)

                    if len(encodings) == 0:
                        st.error("⚠️ **No face detected in snapshot!** Please face the camera directly under good lighting and retake the photo.")
                    elif len(encodings) > 1:
                        st.error("⚠️ **Multiple faces detected!** Please ensure only YOU are in the camera frame.")
                    else:
                        face_emb_list = [float(x) for x in encodings[0]]
                        new_emb_arr = np.array(face_emb_list, dtype=np.float64)

                        all_existing_students = get_all_students()
                        clean_name = new_student_name.strip()
                        clean_phone = new_student_phone.strip()

                        # 1. DUPLICATE CHECK: By Name
                        existing_by_name = next(
                            (s for s in all_existing_students if (s.get('clean_name') or s.get('name', '')).strip().lower() == clean_name.lower()),
                            None
                        )
                        if existing_by_name:
                            st.error(f"❌ **Duplicate Registration!** A student with the name **'{clean_name}'** is already registered (Student ID: #{existing_by_name['student_id']}).")
                            st.info("💡 You cannot register again. Please switch to the **'👤 FaceID Login'** tab to log in.")
                            return

                        # 2. DUPLICATE CHECK: By Facial Biometrics
                        duplicate_biometric_student = None
                        for s in all_existing_students:
                            existing_emb_arr = _parse_embedding(s.get('face_embedding'))
                            if existing_emb_arr is not None:
                                dist = float(np.linalg.norm(existing_emb_arr - new_emb_arr))
                                if dist <= 0.58: # Same person
                                    duplicate_biometric_student = s
                                    break

                        if duplicate_biometric_student:
                            existing_disp = duplicate_biometric_student.get('clean_name') or duplicate_biometric_student.get('name')
                            st.error(f"❌ **Duplicate Face Biometrics!** Your face is already registered in the system as **'{existing_disp}'** (Student ID: #{duplicate_biometric_student['student_id']}).")
                            st.info("💡 Each student can only register once. Please use the **'👤 FaceID Login'** tab to log into your account.")
                            return

                        # Process optional voice embedding
                        voice_emb_list = None
                        if reg_audio is not None:
                            try:
                                audio_bytes = reg_audio.getvalue() if hasattr(reg_audio, "getvalue") else reg_audio.read()
                                v_emb = get_voice_embedding(audio_bytes)
                                if v_emb is not None:
                                    voice_emb_list = [float(x) for x in v_emb]
                            except Exception as ve:
                                print(f"Voice embedding notice: {ve}")

                        # Insert new student into Supabase with phone number
                        created_records = create_student(
                            new_name=clean_name,
                            face_embedding=face_emb_list,
                            voice_embedding=voice_emb_list,
                            phone_number=clean_phone,
                        )

                        if created_records:
                            new_student = created_records[0]
                            train_classifier()

                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = new_student

                            st.success(f"🎉 **Registration Successful! Welcome, {clean_name}!**")
                            time.sleep(1.2)
                            st.rerun()
                        else:
                            st.error("⚠️ Database connection error while saving profile. Please try again.")

        st.markdown("</div>", unsafe_allow_html=True)

    footer_dashboard()