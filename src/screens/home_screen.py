import streamlit as st

def style_landing_page():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Root App Background */
        .stApp {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif !important;
        }

        #MainMenu, footer, header {
            visibility: hidden !important;
        }

        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1280px !important;
        }

        /* Navbar Styling */
        .lp-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 24px;
            background: #090d16;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 32px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }

        .lp-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .lp-logo-badge {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            color: white;
        }

        .lp-logo-text {
            font-family: 'Climate Crisis', sans-serif;
            font-size: 1.4rem;
            color: #ffffff;
            letter-spacing: 0.5px;
        }

        .lp-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #e2e8f0;
        }

        .lp-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 10px #10b981;
        }

        /* Hero Banner */
        .lp-hero {
            text-align: center;
            padding: 40px 20px 20px;
            position: relative;
        }

        .lp-badge-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.25);
            padding: 8px 20px;
            border-radius: 9999px;
            font-size: 0.88rem;
            font-weight: 700;
            color: #4f46e5;
            margin-bottom: 20px;
        }

        .lp-hero-title {
            font-family: 'Outfit', sans-serif !important;
            font-size: 3.8rem !important;
            font-weight: 900 !important;
            line-height: 1.1 !important;
            color: #0f172a !important;
            margin-bottom: 16px !important;
            letter-spacing: -0.03em !important;
        }

        .lp-gradient-text {
            background: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .lp-hero-desc {
            font-size: 1.25rem !important;
            color: #64748b !important;
            max-width: 700px;
            margin: 0 auto 30px !important;
            line-height: 1.6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Role Cards Container */
        .stApp div[data-testid="stColumn"] {
            background-color: #ffffff !important;
            padding: 2.2rem !important;
            border-radius: 28px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04) !important;
            transition: transform 0.25s ease, box-shadow 0.25s ease !important;
        }

        .stApp div[data-testid="stColumn"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08) !important;
        }

        /* Buttons */
        button {
            border-radius: 9999px !important;
            font-weight: 700 !important;
            padding: 12px 24px !important;
            transition: all 0.2s ease !important;
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.25) !important;
        }

        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #3730a3 0%, #4f46e5 100%) !important;
            transform: translateY(-2px);
        }

        button[kind="secondary"] {
            background: #0f172a !important;
            color: white !important;
            border: none !important;
        }

        /* Feature Cards Grid */
        .lp-features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 40px 0;
        }

        .lp-feature-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 28px 24px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.02);
            transition: transform 0.2s;
        }

        .lp-feature-card:hover {
            transform: translateY(-3px);
            border-color: #6366f1;
        }

        .lp-f-icon {
            font-size: 2rem;
            margin-bottom: 12px;
        }

        .lp-f-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 8px;
            font-family: 'Outfit', sans-serif;
        }

        .lp-f-desc {
            font-size: 0.9rem;
            color: #64748b;
            line-height: 1.5;
        }

        /* Tech Section */
        .lp-tech-box {
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            border-radius: 28px;
            padding: 40px 30px;
            color: white;
            text-align: center;
            margin: 40px 0;
        }

        .lp-tech-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 24px;
        }

        .lp-tech-card {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px 16px;
        }

        /* Footer */
        .lp-footer {
            text-align: center;
            padding: 40px 20px 20px;
            color: #94a3b8;
            font-size: 0.88rem;
            border-top: 1px solid #e2e8f0;
            margin-top: 40px;
        }

        @media (max-width: 900px) {
            .lp-hero-title { font-size: 2.6rem !important; }
            .lp-features-grid { grid-template-columns: 1fr; }
            .lp-tech-grid { grid-template-columns: 1fr 1fr; }
        }
        </style>
    """, unsafe_allow_html=True)


def home_screen():
    style_landing_page()

    # 1. NAVBAR
    st.markdown("""
        <div class="lp-navbar">
            <div class="lp-logo">
                <div class="lp-logo-badge">⚡</div>
                <span class="lp-logo-text">SMAPCLASS</span>
            </div>
            <div class="lp-status-pill">
                <span class="lp-dot"></span>
                <span>AI Biometric Engine: Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. HERO SECTION
    st.markdown("""
        <div class="lp-hero">
            <div class="lp-badge-chip">
                <span>✨</span> AI-Powered Classroom Attendance & Analytics
            </div>
            <h1 class="lp-hero-title">Automate Attendance with <span class="lp-gradient-text">AI Vision</span></h1>
            <p class="lp-hero-desc">
                Instant multi-face recognition, voice speaker identification, and automated classroom analytics. Eliminate roll-call delays and proxy attendance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3. QUICK JOIN CODE BAR
    with st.container():
        st.markdown("<p style='text-align: center; font-weight: 600; color: #475569; margin-bottom: 8px;'>🔑 Have a Subject Join Code? Enter below:</p>", unsafe_allow_html=True)
        join_c1, join_c2, join_c3 = st.columns([1, 2, 1])
        with join_c2:
            with st.form("quick_join_form", clear_on_submit=False):
                col_in, col_btn = st.columns([2.5, 1])
                with col_in:
                    quick_code = st.text_input("Join Code", placeholder="E.g. CS301 or MATH-A", label_visibility="collapsed")
                with col_btn:
                    join_submit = st.form_submit_button("Join Class 🚀", type="primary", use_container_width=True)

                if join_submit and quick_code:
                    st.session_state['login_type'] = 'student'
                    st.query_params['join-code'] = quick_code.strip()
                    st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 4. ROLE PORTAL SELECTION (Teacher vs Student)
    st.markdown("<h2 style='text-align: center; font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 24px;'>Choose Your Role</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 14px; margin-bottom: 12px;'>
                <div style='width: 48px; height: 48px; border-radius: 14px; background: #eef2ff; display: flex; align-items: center; justify-content: center; font-size: 1.6rem;'>👨‍🏫</div>
                <div>
                    <span style='font-size: 0.75rem; font-weight: 800; color: #4f46e5; text-transform: uppercase; letter-spacing: 1px;'>Faculty Portal</span>
                    <h3 style='margin: 0; font-size: 1.5rem; font-weight: 800; color: #0f172a;'>I am a Teacher</h3>
                </div>
            </div>
            <p style='color: #64748b; font-size: 0.95rem; margin-bottom: 20px; line-height: 1.5;'>
                Create subjects, take AI classroom photo attendance, run voice speaker recognition, and generate dynamic QR codes.
            </p>
            <ul style='color: #475569; font-size: 0.88rem; padding-left: 18px; margin-bottom: 24px; line-height: 1.8;'>
                <li><b>✓</b> AI Classroom Group Photo Scan</li>
                <li><b>✓</b> Voice Audio Speaker Attendance</li>
                <li><b>✓</b> Subject QR Codes & Roster Sync</li>
            </ul>
        """, unsafe_allow_html=True)
        
        if st.button("Open Teacher Portal 👨‍🏫", type="primary", use_container_width=True, key="btn_teacher_portal"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with col2:
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 14px; margin-bottom: 12px;'>
                <div style='width: 48px; height: 48px; border-radius: 14px; background: #fdf2f8; display: flex; align-items: center; justify-content: center; font-size: 1.6rem;'>🎓</div>
                <div>
                    <span style='font-size: 0.75rem; font-weight: 800; color: #ec4899; text-transform: uppercase; letter-spacing: 1px;'>Student Portal</span>
                    <h3 style='margin: 0; font-size: 1.5rem; font-weight: 800; color: #0f172a;'>I am a Student</h3>
                </div>
            </div>
            <p style='color: #64748b; font-size: 0.95rem; margin-bottom: 20px; line-height: 1.5;'>
                Instant 1-second FaceID login, enroll in subjects with join codes, check daily attendance status, and manage voice profiles.
            </p>
            <ul style='color: #475569; font-size: 0.88rem; padding-left: 18px; margin-bottom: 24px; line-height: 1.8;'>
                <li><b>✓</b> 1-Second Biometric FaceID Login</li>
                <li><b>✓</b> 1-Click Subject Enrollment</li>
                <li><b>✓</b> Live Attendance Record & Percentage</li>
            </ul>
        """, unsafe_allow_html=True)
        
        if st.button("Open Student Portal 🎓", type="secondary", use_container_width=True, key="btn_student_portal"):
            st.session_state['login_type'] = 'student'
            st.rerun()

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # 5. CORE FEATURES GRID
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <span style='font-size: 0.8rem; font-weight: 800; color: #4f46e5; text-transform: uppercase; letter-spacing: 1.5px;'>STATE-OF-THE-ART FEATURES</span>
            <h2 style='font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-top: 4px;'>Built for High-Precision Classrooms</h2>
        </div>

        <div class="lp-features-grid">
            <div class="lp-feature-card">
                <div class="lp-f-icon">⚡</div>
                <div class="lp-f-title">Multi-Face Recognition</div>
                <div class="lp-f-desc">Extracts 128-D facial vectors and matches multiple student faces in group photos simultaneously.</div>
            </div>
            <div class="lp-feature-card">
                <div class="lp-f-icon">🎙️</div>
                <div class="lp-f-title">AI Voice Attendance</div>
                <div class="lp-f-desc">Deep speaker embeddings via Resemblyzer identify speaking students from classroom voice notes.</div>
            </div>
            <div class="lp-feature-card">
                <div class="lp-f-icon">📲</div>
                <div class="lp-f-title">Dynamic QR Auto-Enroll</div>
                <div class="lp-f-desc">Instant subject join codes and QR codes allow fast, seamless onboarding directly into rosters.</div>
            </div>
            <div class="lp-feature-card">
                <div class="lp-f-icon">📊</div>
                <div class="lp-f-title">Live Attendance Ledger</div>
                <div class="lp-f-desc">Real-time attendance logs, percentage tracking, and historical summary analytics.</div>
            </div>
            <div class="lp-feature-card">
                <div class="lp-f-icon">🔒</div>
                <div class="lp-f-title">Encrypted Biometrics</div>
                <div class="lp-f-desc">Photos are converted to mathematical vectors. Raw images are never exposed or shared.</div>
            </div>
            <div class="lp-feature-card">
                <div class="lp-f-icon">☁️</div>
                <div class="lp-f-title">Supabase Cloud Sync</div>
                <div class="lp-f-desc">PostgreSQL-powered backend with real-time vector indexing and secure student authentication.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 6. TECH ARCHITECTURE
    st.markdown("""
        <div class="lp-tech-box">
            <span style='font-size: 0.8rem; font-weight: 800; color: #818cf8; text-transform: uppercase; letter-spacing: 1.5px;'>UNDER THE HOOD</span>
            <h2 style='font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 6px 0 12px;'>Engineered for Speed & Scale</h2>
            <p style='color: #cbd5e1; max-width: 650px; margin: 0 auto 20px; font-size: 0.95rem;'>
                Built on industry-standard computer vision and deep learning pipelines with PostgreSQL storage.
            </p>
            <div class="lp-tech-grid">
                <div class="lp-tech-card">
                    <div style='font-size: 1.8rem;'>🐍</div>
                    <div style='font-weight: 700; color: #fff; margin-top: 6px;'>Streamlit & Python</div>
                    <div style='font-size: 0.78rem; color: #94a3b8; margin-top: 4px;'>Interactive Web Framework</div>
                </div>
                <div class="lp-tech-card">
                    <div style='font-size: 1.8rem;'>👁️</div>
                    <div style='font-weight: 700; color: #fff; margin-top: 6px;'>dlib & SVM</div>
                    <div style='font-size: 0.78rem; color: #94a3b8; margin-top: 4px;'>128-D Face Vectorizer</div>
                </div>
                <div class="lp-tech-card">
                    <div style='font-size: 1.8rem;'>🎙️</div>
                    <div style='font-weight: 700; color: #fff; margin-top: 6px;'>Resemblyzer</div>
                    <div style='font-size: 0.78rem; color: #94a3b8; margin-top: 4px;'>Voice Speaker AI</div>
                </div>
                <div class="lp-tech-card">
                    <div style='font-size: 1.8rem;'>🗄️</div>
                    <div style='font-weight: 700; color: #fff; margin-top: 6px;'>Supabase Cloud</div>
                    <div style='font-size: 0.78rem; color: #94a3b8; margin-top: 4px;'>PostgreSQL & Vector DB</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 7. FOOTER
    st.markdown("""
        <div class="lp-footer">
            <p>© 2026 <b>SMAPCLASS</b> • Unified AI Classroom Intelligence System • All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)
