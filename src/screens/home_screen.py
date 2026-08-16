import streamlit as st
import textwrap
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def render_html(html_content):
    """Renders HTML cleanly without Markdown code-block indentation issues."""
    clean_html = textwrap.dedent(html_content).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)


def home_screen():
    style_base_layout()
    style_background_home()

    # Top Brand Header
    header_home()

    # Hero Banner
    render_html("""
    <div style="text-align: center; margin: 1.5rem 0 2rem 0;">
        <div style="display: inline-block; background: rgba(88, 101, 242, 0.15); border: 1px solid rgba(88, 101, 242, 0.35); padding: 6px 18px; border-radius: 100px; color: #a5b4fc; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1rem;">
            ✨ AI-Powered Biometric Attendance & Classroom Analytics
        </div>
        <h1 style="color: #ffffff; font-size: 2.8rem; line-height: 1.15; margin-bottom: 0.8rem;">
            Automate & Elevate Your <span style="background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Classroom</span>
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 720px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
            Real-time facial & voice recognition attendance, automatic roster syncing, dynamic QR code enrollment, and instant classroom insights powered by deep machine learning.
        </p>
    </div>
    """)

    # Quick Join Code Box
    with st.container():
        render_html("""
        <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 18px; padding: 1.2rem 1.8rem; margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
            <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem; display: flex; align-items: center; gap: 8px;">
                <span>⚡</span> Instant Subject Auto-Join
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem;">
                Have a class join code from your instructor? Enter it below to directly enroll:
            </div>
        </div>
        """)

        jc_col1, jc_col2 = st.columns([3, 1], vertical_alignment="center")
        with jc_col1:
            quick_code = st.text_input(
                "Join Code",
                placeholder="Enter Subject Join Code (e.g. CS301)...",
                label_visibility="collapsed",
                key="home_quick_join_input",
            )
        with jc_col2:
            if st.button("Join Class 🚀", type="primary", use_container_width=True, key="home_quick_join_btn"):
                if quick_code and quick_code.strip():
                    clean_code = quick_code.strip()
                    st.session_state['login_type'] = 'student'
                    st.session_state['pending_join_code'] = clean_code
                    st.query_params['join-code'] = clean_code
                    st.rerun()
                else:
                    st.warning("Please enter a valid Subject Code.")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Role Selection Portals Grid
    render_html("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #ffffff; font-size: 1.8rem; margin-bottom: 0.4rem;">Choose Your Portal</h2>
        <p style="color: #94a3b8; font-size: 0.95rem;">Select your dashboard to manage classroom sessions or enroll as a student.</p>
    </div>
    """)

    col1, col2 = st.columns(2, gap="large")

    # Faculty / Teacher Portal Card
    with col1:
        render_html("""
        <div class="landing-portal-card">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <span class="portal-badge teacher">👨‍🏫 Faculty & Instructors</span>
                    <span style="font-size: 2.2rem;">👨‍🏫</span>
                </div>
                <h3 style="color: #ffffff; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.6rem;">Teacher Portal</h3>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin-bottom: 1.2rem;">
                    Create subjects, manage enrolled student rosters, batch analyze classroom attendance photos, and run voice speaker recognition.
                </p>
                <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1rem; margin-bottom: 1.5rem;">
                    <div class="feature-chip"><span class="check-icon">✓</span> AI Classroom Photo & Group Scan</div>
                    <div class="feature-chip"><span class="check-icon">✓</span> Voice Audio Speaker Identification</div>
                    <div class="feature-chip"><span class="check-icon">✓</span> Subject Management & Instant QR Codes</div>
                    <div class="feature-chip"><span class="check-icon">✓</span> Historical Attendance Logs & CSV Export</div>
                </div>
            </div>
        </div>
        """)

        if st.button("Open Teacher Dashboard 👨‍🏫", type="primary", use_container_width=True, key="btn_portal_teacher"):
            st.session_state['login_type'] = 'teacher'
            st.query_params['role'] = 'teacher'
            st.rerun()

    # Student FaceID Portal Card
    with col2:
        render_html("""
        <div class="landing-portal-card">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <span class="portal-badge student">🎓 Students & Learners</span>
                    <span style="font-size: 2.2rem;">🎓</span>
                </div>
                <h3 style="color: #ffffff; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.6rem;">Student Portal</h3>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin-bottom: 1.2rem;">
                    Enroll in subjects with one-click Join Codes or QR scans, register your facial biometrics and voice signature for instant attendance.
                </p>
                <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1rem; margin-bottom: 1.5rem;">
                    <div class="feature-chip"><span class="check-icon">✓</span> Biometric Face Login & Verification</div>
                    <div class="feature-chip"><span class="check-icon">✓</span> Instant Subject Join via Code or QR</div>
                    <div class="feature-chip"><span class="check-icon">✓</span> Personal Attendance Percentage & Logs</div>
                    <div class="feature-chip"><span class="check-icon">✓</span> Voice Profile & Audio Sample Enrollment</div>
                </div>
            </div>
        </div>
        """)

        if st.button("Open Student Portal 🎓", type="secondary", use_container_width=True, key="btn_portal_student"):
            st.session_state['login_type'] = 'student'
            st.query_params['role'] = 'student'
            st.rerun()

    # Features Showcase Matrix
    render_html("""
    <div style="margin-top: 3.5rem; text-align: center;">
        <h2 style="color: #ffffff; font-size: 1.7rem; margin-bottom: 0.5rem;">Built for High-Precision Classrooms</h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 2rem;">Enterprise AI architecture engineered for accuracy, speed, and privacy.</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; text-align: left;">
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">⚡</div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem;">Multi-Face Attendance</div>
                <div style="color: #94a3b8; font-size: 0.86rem; line-height: 1.5;">Recognize multiple students in a single classroom frame simultaneously in milliseconds using 128-d biometric embeddings.</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🎙️</div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem;">AI Voice Attendance</div>
                <div style="color: #94a3b8; font-size: 0.86rem; line-height: 1.5;">Integrated Resemblyzer speaker recognition identifies speaking students directly from classroom audio clips.</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📲</div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem;">Instant QR Auto-Enroll</div>
                <div style="color: #94a3b8; font-size: 0.86rem; line-height: 1.5;">Generate unique subject join links and dynamic QR codes for rapid student onboarding into rosters.</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem;">Supabase Real-Time DB</div>
                <div style="color: #94a3b8; font-size: 0.86rem; line-height: 1.5;">Cloud-native PostgreSQL database handles high-concurrency attendance logs and biometric vector indices.</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🔒</div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem;">Encrypted Biometrics</div>
                <div style="color: #94a3b8; font-size: 0.86rem; line-height: 1.5;">Photos & audio are transformed into cryptographic mathematical vector embeddings. Raw media is never stored insecurely.</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🌐</div>
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.3rem;">Universal Hardware</div>
                <div style="color: #94a3b8; font-size: 0.86rem; line-height: 1.5;">Compatible with standard laptops, webcams, smartphones, and classroom cameras without specialized sensor hardware.</div>
            </div>
        </div>
    </div>
    """)

    # Footer
    footer_home()