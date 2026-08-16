import base64
import streamlit as st
import numpy as np
from datetime import datetime
import pandas as pd
import time

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
    get_all_students,
    enroll_student_to_subject,
    get_defaulter_students_for_teacher,
    parse_student_details,
)
from src.database.materials import (
    upload_subject_pdf,
    get_subject_materials,
    delete_subject_pdf,
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
from src.database.config import supabase
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.services.sms_service import (
    format_attendance_warning_sms,
    generate_sms_intent_url,
    generate_whatsapp_intent_url,
    send_sms_via_gateway,
)


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns([1.2, 1.8], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        sub_c1, sub_c2 = st.columns([2, 1], vertical_alignment='center')
        with sub_c1:
            st.markdown(f"<div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>Welcome, {teacher_data['name']} 👋</div>", unsafe_allow_html=True)
        with sub_c2:
            if st.button("🚪 Logout", type='secondary', key='loginbackbtn', use_container_width=True):
                st.session_state['is_logged_in'] = False
                if 'teacher_data' in st.session_state:
                    del st.session_state.teacher_data
                st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    # Check defaulters count for tab badge
    teacher_id = teacher_data['teacher_id']
    defaulters_preview = get_defaulter_students_for_teacher(teacher_id, threshold=75.0)
    defaulter_count = len(defaulters_preview)

    tab1, tab2, tab3, tab4 = st.columns(4)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('📸 Take Attendance', type=type1, use_container_width=True):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('📚 Subjects & PDFs', type=type2, use_container_width=True):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('📊 Records', type=type3, use_container_width=True):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    with tab4:
        type4 = "primary" if st.session_state.current_teacher_tab == 'low_attendance' else "tertiary"
        tab4_label = f"⚠️ SMS Alert ({defaulter_count})" if defaulter_count > 0 else "⚠️ SMS Alert (<75%)"
        if st.button(tab4_label, type=type4, use_container_width=True):
            st.session_state.current_teacher_tab = 'low_attendance'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
    elif st.session_state.current_teacher_tab == "low_attendance":
        teacher_tab_low_attendance()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown("<h2 style='color: #1e293b; font-size: 1.6rem; margin-bottom: 1rem;'>Take AI Attendance (Group & Single Scan)</h2>", unsafe_allow_html=True)

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You haven\'t created any subjects yet! Please create one in the "Manage Subjects" tab to begin!')
        return

    subject_options = {f"{s['name']} ({s['subject_code']}) - Sec {s.get('section', 'A')}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('➕ Add Photos', type='primary', use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.markdown("<h3 style='color: #1e293b; font-size: 1.2rem; margin-bottom: 0.8rem;'>Classroom Group Photos Added</h3>", unsafe_allow_html=True)
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Classroom Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('🗑️ Clear all photos', use_container_width=True, type='tertiary', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('⚡ Run Face Analysis', use_container_width=True, type='secondary', disabled=not has_photos):
            with st.spinner('Deep scanning classroom group photos for all students...'):
                all_detected_ids = {}
                total_faces_detected_across_photos = 0

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, num_faces = predict_attendance(img_np)
                    total_faces_detected_across_photos += num_faces

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                # 1. Fetch currently enrolled students in this subject
                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data or []

                # 2. Also check if any detected registered student is in this classroom but not in the subject roster yet
                all_registered = get_all_students()
                all_students_map = {s['student_id']: s for s in all_registered}
                enrolled_sids = set(node['students']['student_id'] for node in enrolled_students if node.get('students'))

                # Auto-enroll any detected student who is in class
                for detected_sid in all_detected_ids.keys():
                    if detected_sid not in enrolled_sids and detected_sid in all_students_map:
                        try:
                            enroll_student_to_subject(detected_sid, selected_subject_id)
                            enrolled_sids.add(detected_sid)
                        except Exception as ee:
                            print(f"Auto-enroll notice: {ee}")

                # Refresh enrolled students after auto-enrolling present students
                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data or []

                if not enrolled_students and not all_detected_ids:
                    st.warning('No enrolled or registered students were found in the database. Please ensure students are registered.')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node.get('students')
                        if not student:
                            continue
                        sid_val = student['student_id']
                        parsed = parse_student_details(student)
                        sources = all_detected_ids.get(int(sid_val), []) or all_detected_ids.get(str(sid_val), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": parsed['name'],
                            "ID": student['student_id'],
                            "Phone": parsed['phone_number'],
                            "Source": ", ".join(sources) if is_present else "Not in Photo",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('🎙️ Use Voice Attendance', type='primary', use_container_width=True):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns([2, 1], vertical_alignment='center')
    with col1:
        st.markdown("<h2 style='color: #1e293b; font-size: 1.6rem; margin: 0;'>Manage Subjects & Study Materials</h2>", unsafe_allow_html=True)
    with col2:
        if st.button('➕ Create New Subject', type='primary', use_container_width=True):
            create_subject_dialog(teacher_id)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            s_id = sub['subject_id']
            s_name = sub['name']
            s_code = sub['subject_code']
            s_sec = sub['section']

            # Get materials count for this subject
            mats = get_subject_materials(s_id)
            mat_count = len(mats)

            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
                ("📄", "PDF Notes", mat_count),
            ]

            def make_share_btn(name_val=s_name, code_val=s_code):
                if st.button(f"🔗 Share Code: {code_val}", key=f"share_{code_val}", use_container_width=True):
                    share_subject_dialog(name_val, code_val)

            subject_card(
                name=s_name,
                code=s_code,
                section=s_sec,
                stats=stats,
                footer_callback=make_share_btn
            )

            # Course Materials & PDF Upload Accordion for this Subject
            with st.expander(f"📄 Upload & Manage PDF Notes for {s_name} ({mat_count} active)", expanded=False):
                up_col1, up_col2 = st.columns([2, 1], vertical_alignment="bottom")
                with up_col1:
                    pdf_title = st.text_input(f"Document Title", placeholder="e.g. Unit 1: Introduction to Data Structures", key=f"title_{s_id}")
                    uploaded_pdf = st.file_uploader(f"Choose PDF File", type=["pdf"], key=f"pdf_up_{s_id}")
                with up_col2:
                    if st.button("📤 Upload PDF to Students", type="primary", use_container_width=True, key=f"btn_up_{s_id}"):
                        if uploaded_pdf is not None:
                            with st.spinner("Uploading and syncing PDF with all enrolled students..."):
                                pdf_bytes = uploaded_pdf.getvalue()
                                filename = uploaded_pdf.name
                                doc_title = pdf_title.strip() if pdf_title and pdf_title.strip() else filename
                                upload_subject_pdf(s_id, teacher_id, doc_title, filename, pdf_bytes)
                                st.toast(f"✅ '{filename}' uploaded successfully for all enrolled students!", icon="🎉")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Please select a PDF file to upload.")

                # List currently uploaded PDFs for this subject
                if mats:
                    st.markdown("<div style='font-weight: 600; color: #1e293b; margin-top: 1rem; margin-bottom: 0.5rem;'>Active PDFs for Enrolled Students:</div>", unsafe_allow_html=True)
                    for m in mats:
                        m_id = m['id']
                        m_title = m['title']
                        m_fname = m['filename']
                        m_size = m['file_size']
                        m_date = m.get('uploaded_at', '')[:10]

                        card_c1, card_c2, card_c3 = st.columns([3, 1, 1], vertical_alignment="center")
                        with card_c1:
                            st.markdown(f"**📄 {m_title}** &nbsp;•&nbsp; `<small>{m_fname} ({m_size}) - {m_date}</small>`", unsafe_allow_html=True)
                        with card_c2:
                            if m.get('file_data'):
                                raw_bytes = base64.b64decode(m['file_data'])
                                st.download_button(
                                    label="⬇️ Download",
                                    data=raw_bytes,
                                    file_name=m_fname,
                                    mime="application/pdf",
                                    key=f"dl_t_{s_id}_{m_id}",
                                    use_container_width=True
                                )
                        with card_c3:
                            if st.button("🗑️ Delete", key=f"del_{s_id}_{m_id}", use_container_width=True, type="secondary"):
                                delete_subject_pdf(m_id, s_id)
                                st.toast(f"🗑️ '{m_fname}' deleted from portal for all students!", icon="⚠️")
                                time.sleep(1)
                                st.rerun()
                else:
                    st.caption("ℹ️ No PDF notes uploaded yet for this subject. Upload lecture slides or notes above.")

            st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    else:
        st.info("No subjects found. Click **'➕ Create New Subject'** above to create your first class!")


def teacher_tab_attendance_records():
    st.markdown("<h2 style='color: #1e293b; font-size: 1.6rem; margin-bottom: 1rem;'>Attendance Records</h2>", unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet. Take attendance using photo scan or voice recognition to view historical logs here.")
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + ' Students Present'
    )

    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']])

    st.dataframe(display_df, use_container_width=True, hide_index=True)


def teacher_tab_low_attendance():
    """Defaulter List & Automated SMS Warning System for Students with Attendance < 75%."""
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown("<h2 style='color: #1e293b; font-size: 1.6rem; margin-bottom: 0.4rem;'>⚠️ Low Attendance Alerts & SMS Dispatch (< 75%)</h2>", unsafe_allow_html=True)
    st.caption("Identify students whose attendance is below the mandatory 75% threshold and dispatch instant SMS attendance warnings.")

    with st.spinner("Analyzing attendance percentages across your courses..."):
        defaulters = get_defaulter_students_for_teacher(teacher_id, threshold=75.0)

    if not defaulters:
        st.markdown("""
            <div style="background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 16px; padding: 1.8rem; text-align: center; margin: 1.5rem 0;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🎉</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #065f46; margin-bottom: 0.4rem;">Excellent! No Low Attendance Defaulters Found</div>
                <div style="color: #047857; font-size: 0.92rem;">All enrolled students currently maintain an attendance rate of <b>75% or higher</b> in your subjects.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🚨 Defaulter Count (< 75%)", value=f"{len(defaulters)} Students", delta="Action Required", delta_color="inverse")
    with m2:
        avg_pct = round(sum(d['percentage'] for d in defaulters) / len(defaulters), 1)
        st.metric(label="📉 Avg Defaulter Attendance", value=f"{avg_pct}%")
    with m3:
        st.metric(label="📋 Mandatory Threshold", value="75.0%")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Batch SMS Action Header
    batch_c1, batch_c2 = st.columns([2.5, 1.5], vertical_alignment="center")
    with batch_c1:
        st.markdown(f"**Found {len(defaulters)} student(s) requiring immediate attendance warning:**")
    with batch_c2:
        if st.button("🚀 Send SMS to ALL Defaulters", type="primary", use_container_width=True, key="btn_send_all_sms"):
            sent_count = 0
            with st.spinner(f"Dispatching SMS alerts to {len(defaulters)} student(s)..."):
                for d in defaulters:
                    phone = d['phone_number']
                    if phone and phone != "N/A":
                        msg = format_attendance_warning_sms(
                            d['name'], d['subject_name'], d['percentage'], d['attended_classes'], d['total_classes']
                        )
                        success, resp = send_sms_via_gateway(phone, msg)
                        if success:
                            sent_count += 1
                st.toast(f"✅ Automated SMS warnings dispatched to {sent_count} student(s)!", icon="📲")
                time.sleep(1.5)
                st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Defaulter Student Cards & Individual Actions
    for idx, d in enumerate(defaulters):
        st.markdown(f"""
            <div style="background: white; border: 1.5px solid #fecaca; border-left: 6px solid #ef4444; border-radius: 14px; padding: 18px 22px; margin-bottom: 14px; box-shadow: 0 2px 6px rgba(239, 68, 68, 0.06);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 700; color: #1e293b;">{d['name']} <span style="font-size: 0.85rem; font-weight: 600; color: #64748b;">(ID: #{d['student_id']})</span></div>
                        <div style="color: #475569; font-size: 0.9rem; margin-top: 4px;">
                            📚 Subject: <b>{d['subject_name']} ({d['subject_code']})</b> &nbsp;•&nbsp; Section: <b>{d['section']}</b>
                        </div>
                        <div style="color: #64748b; font-size: 0.88rem; margin-top: 4px;">
                            📱 Mobile: <span style="background: #f1f5f9; padding: 2px 8px; border-radius: 5px; font-weight: 600; color: #1e293b;">{d['phone_number']}</span>
                            &nbsp;•&nbsp; 📊 Attended: <b>{d['attended_classes']} / {d['total_classes']} classes</b> ({d['missed_classes']} missed)
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; padding: 6px 14px; border-radius: 20px; font-weight: 800; font-size: 1.05rem; display: inline-block;">
                            ⚠️ {d['percentage']}%
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        msg_body = format_attendance_warning_sms(
            d['name'], d['subject_name'], d['percentage'], d['attended_classes'], d['total_classes']
        )
        sms_url = generate_sms_intent_url(d['phone_number'], msg_body)
        wa_url = generate_whatsapp_intent_url(d['phone_number'], msg_body)

        btn_c1, btn_c2, btn_c3 = st.columns([1.5, 1.5, 1.5])
        with btn_c1:
            if st.button(f"🚀 Send Direct SMS", key=f"btn_sms_{idx}_{d['student_id']}", use_container_width=True, type="secondary"):
                if d['phone_number'] and d['phone_number'] != "N/A":
                    success, resp = send_sms_via_gateway(d['phone_number'], msg_body)
                    st.toast(f"✅ SMS sent to {d['name']} ({d['phone_number']})!", icon="📲")
                else:
                    st.error("❌ No phone number registered for this student.")

        with btn_c2:
            st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration: none;"><button style="width: 100%; border-radius: 12px; background: #25D366; color: white; border: none; padding: 0.6rem 1rem; font-weight: 600; cursor: pointer;">💬 WhatsApp Alert</button></a>', unsafe_allow_html=True)

        with btn_c3:
            st.markdown(f'<a href="{sms_url}" style="text-decoration: none;"><button style="width: 100%; border-radius: 12px; background: #3b82f6; color: white; border: none; padding: 0.6rem 1rem; font-weight: 600; cursor: pointer;">📱 Open SMS App</button></a>', unsafe_allow_html=True)

        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def teacher_screen_login():
    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', use_container_width=True):
            st.session_state['login_type'] = None
            st.query_params.clear()
            st.rerun()

    st.markdown("""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 18px; padding: 2rem; box-shadow: 0 4px 16px rgba(0,0,0,0.04); margin-top: 1rem;">
            <h2 style="color: #1e293b; font-size: 1.5rem; text-align: center; margin-bottom: 0.4rem;">Faculty Login</h2>
            <p style="color: #64748b; font-size: 0.9rem; text-align: center; margin-bottom: 1.5rem;">Enter your faculty credentials to manage your classroom sessions.</p>
    """, unsafe_allow_html=True)

    teacher_username = st.text_input("Username", placeholder='Enter username (e.g. TezasSingh)', key='t_login_user')
    teacher_pass = st.text_input("Password", type='password', placeholder="Enter password", key='t_login_pwd')

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button('🔑 Login', use_container_width=True, type='primary'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with btnc2:
        if st.button('📝 Register Instead', type="secondary", use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username is already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully created profile! Please login."
    except Exception as e:
        return False, "Unexpected registration error."


def teacher_screen_register():
    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', use_container_width=True):
            st.session_state['login_type'] = None
            st.query_params.clear()
            st.rerun()

    st.markdown("""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 18px; padding: 2rem; box-shadow: 0 4px 16px rgba(0,0,0,0.04); margin-top: 1rem;">
            <h2 style="color: #1e293b; font-size: 1.5rem; text-align: center; margin-bottom: 0.4rem;">Register Faculty Profile</h2>
            <p style="color: #64748b; font-size: 0.9rem; text-align: center; margin-bottom: 1.5rem;">Create a new instructor profile to create classes and take automated attendance.</p>
    """, unsafe_allow_html=True)

    teacher_username = st.text_input("Username", placeholder='e.g. abhinavsingh', key='t_reg_user')
    teacher_name = st.text_input("Full Name", placeholder='e.g. Abhinav Singh', key='t_reg_name')
    teacher_pass = st.text_input("Password", type='password', placeholder="Enter password", key='t_reg_pwd')
    teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="Confirm password", key='t_reg_pwd_conf')

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button('📝 Register Now', type='primary', use_container_width=True):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button('🔑 Login Instead', type="secondary", use_container_width=True):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    footer_dashboard()