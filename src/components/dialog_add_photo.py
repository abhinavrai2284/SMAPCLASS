import streamlit as st
from PIL import Image

@st.dialog("📸 Classroom Photo Capture (Full-Screen)", width="large")
def add_photos_dialog():
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    st.markdown("""
        <div style="margin-bottom: 0.8rem;">
            <div style="font-weight: 700; color: #1e293b; font-size: 1.1rem;">Take Full-Screen Classroom Photo</div>
            <div style="color: #64748b; font-size: 0.88rem;">Capture high-resolution group photos of students in class to run AI Face Attendance.</div>
        </div>
    """, unsafe_allow_html=True)

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('📷 Live Camera', type=type_camera, use_container_width=True):
            st.session_state.photo_tab = 'camera'
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('📁 Upload Photos', type=type_upload, use_container_width=True):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Capture classroom snapshot', key='dialog_cam')
        if cam_photo:
            img = Image.open(cam_photo).convert('RGB')
            st.session_state.attendance_images.append(img)
            st.toast(f'✅ Photo #{len(st.session_state.attendance_images)} Captured Successfully!', icon='📸')
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader('Select classroom image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')
        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f).convert('RGB'))
            st.toast(f'✅ {len(uploaded_files)} photo(s) added!', icon='📁')
            st.rerun()

    st.divider()

    count = len(st.session_state.attendance_images)
    done_label = f"✨ Done ({count} Photo{'s' if count != 1 else ''} Ready)" if count > 0 else "Done"
    if st.button(done_label, type='primary', use_container_width=True):
        st.rerun()