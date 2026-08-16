import streamlit as st
import os

def load_landing_styles():
    # Read the exact styles.css file
    css_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "static", "img", "css", "styles.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "static", "css", "styles.css")

    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap');

        /* Streamlit Overrides */
        #MainMenu, footer, header {{
            visibility: hidden !important;
        }}

        .stApp {{
            background-color: #fcfcfd !important;
        }}

        .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}

        /* Apply exact landing page styles */
        {css_content}

        /* Streamlit Button Restyling for Role Cards */
        .stApp div[data-testid="stColumn"] button {{
            width: 100% !important;
            padding: 16px 28px !important;
            border-radius: 100px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            font-family: 'Outfit', sans-serif !important;
            transition: all 0.2s ease !important;
        }}

        .stApp div[data-testid="stColumn"] button[kind="primary"] {{
            background: #000000 !important;
            color: #ffffff !important;
            border: none !important;
        }}

        .stApp div[data-testid="stColumn"] button[kind="primary"]:hover {{
            background: #333333 !important;
            transform: translateY(-2px) !important;
        }}

        .stApp div[data-testid="stColumn"] button[kind="secondary"] {{
            background: #1e1e2f !important;
            color: #ffffff !important;
            border: none !important;
        }}

        .stApp div[data-testid="stColumn"] button[kind="secondary"]:hover {{
            background: #2a2a4a !important;
            transform: translateY(-2px) !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def home_screen():
    load_landing_styles()

    # 1. NAVIGATION BAR
    st.markdown("""
        <header class="navbar">
            <div class="logo">
                <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="SMAPCLASS Logo" style="height: 38px; width: auto;">
                <span class="logo-text">SMAPCLASS</span>
            </div>
            <nav class="nav-links">
                <a href="#hero">Home</a>
                <a href="#portals">Portals</a>
                <a href="#features">Features</a>
                <a href="#workflow">How It Works</a>
                <a href="#tech">Tech Stack</a>
            </nav>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div class="status-pill" title="AI Biometric Engine Active">
                    <span class="status-dot online"></span>
                    <span>AI Engine: Active</span>
                </div>
            </div>
        </header>
    """, unsafe_allow_html=True)

    # 2. HERO SECTION
    st.markdown("""
        <section class="hero" id="hero">
            <!-- Floating Left Card -->
            <div class="floating-card card-left">
                <svg viewBox="0 0 300 240" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; border-radius: 20px; background: linear-gradient(135deg, #1e1e2f 0%, #2a2a4a 100%);">
                    <rect width="300" height="240" rx="16" fill="#121324"/>
                    <circle cx="150" cy="90" r="45" fill="#5865F2" fill-opacity="0.2" stroke="#5865F2" stroke-width="2"/>
                    <circle cx="150" cy="80" r="22" fill="#5865F2"/>
                    <path d="M125 120C125 106 136 98 150 98C164 98 175 106 175 120" stroke="#5865F2" stroke-width="3" stroke-linecap="round"/>
                    <path d="M100 50 H90 V60" stroke="#4BB786" stroke-width="3" stroke-linecap="round"/>
                    <path d="M200 50 H210 V60" stroke="#4BB786" stroke-width="3" stroke-linecap="round"/>
                    <path d="M100 130 H90 V120" stroke="#4BB786" stroke-width="3" stroke-linecap="round"/>
                    <path d="M200 130 H210 V120" stroke="#4BB786" stroke-width="3" stroke-linecap="round"/>
                    <rect x="50" y="160" width="200" height="30" rx="8" fill="#1e293b"/>
                    <text x="150" y="180" font-family="'Outfit', sans-serif" font-size="12" fill="#4BB786" font-weight="700" text-anchor="middle">✓ MATCHED • 99.8% ACCURACY</text>
                    <text x="150" y="212" font-family="'Outfit', sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Aarav Sharma • ID #2026-CS-42</text>
                </svg>
            </div>

            <!-- Floating Right Card -->
            <div class="floating-card card-right">
                <svg viewBox="0 0 300 240" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; border-radius: 20px; background: linear-gradient(135deg, #181926 0%, #20223a 100%);">
                    <rect width="300" height="240" rx="16" fill="#121324"/>
                    <text x="24" y="38" font-family="'Outfit', sans-serif" font-size="14" fill="#ffffff" font-weight="700">Live Class Metrics</text>
                    <rect x="220" y="24" width="56" height="20" rx="10" fill="#4BB786" fill-opacity="0.2"/>
                    <text x="248" y="38" font-family="'Outfit', sans-serif" font-size="10" fill="#4BB786" font-weight="700" text-anchor="middle">LIVE</text>
                    <rect x="30" y="140" width="28" height="50" rx="6" fill="#5865F2"/>
                    <rect x="70" y="110" width="28" height="80" rx="6" fill="#5865F2"/>
                    <rect x="110" y="90" width="28" height="100" rx="6" fill="#5865F2"/>
                    <rect x="150" y="70" width="28" height="120" rx="6" fill="#5865F2"/>
                    <rect x="190" y="85" width="28" height="105" rx="6" fill="#4BB786"/>
                    <rect x="230" y="60" width="28" height="130" rx="6" fill="#EB459E"/>
                    <text x="30" y="215" font-family="'Outfit', sans-serif" font-size="12" fill="#cbd5e1" font-weight="600">Present: 96%</text>
                    <text x="180" y="215" font-family="'Outfit', sans-serif" font-size="12" fill="#4BB786" font-weight="600">48 / 50 Present</text>
                </svg>
            </div>

            <div class="badge">✨ AI-Powered Biometric Attendance & Analytics</div>
            <h1>Automate & Elevate Your <span>Classroom</span></h1>
            <p>Real-time facial & voice recognition attendance, automatic roster syncing, and instant classroom insights powered by deep machine learning.</p>
        </section>
    """, unsafe_allow_html=True)

    # 3. INTERACTIVE JOIN CODE FORM
    c_pad1, c_form, c_pad2 = st.columns([1, 2, 1])
    with c_form:
        with st.form("join_form_hero", clear_on_submit=False):
            st.markdown("<p style='text-align: center; font-weight: 700; color: #475569; margin-bottom: 4px;'>🔑 Have a Subject Join Code? Enter below:</p>", unsafe_allow_html=True)
            col_in, col_btn = st.columns([2.5, 1])
            with col_in:
                join_code_val = st.text_input("Join Code", placeholder="E.g. CS301", label_visibility="collapsed")
            with col_btn:
                submitted = st.form_submit_button("Join Class 🚀", type="primary", use_container_width=True)

            if submitted and join_code_val:
                st.session_state['login_type'] = 'student'
                st.query_params['join-code'] = join_code_val.strip()
                st.rerun()

    # 4. INTEGRATED LOGO STRIP
    st.markdown("""
        <div class="integrated" style="margin-bottom: 60px;">
            <p>INTEGRATED WITH MODERN LMS & BIOMETRIC ENGINES</p>
            <div class="logo-strip">
                <span style="font-weight: 700; color: #64748b; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="#64748b"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg> Supabase Cloud
                </span>
                <span style="font-weight: 700; color: #64748b; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="#64748b"><circle cx="12" cy="12" r="9"/></svg> dlib Face Vectorizer
                </span>
                <span style="font-weight: 700; color: #64748b; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="#64748b"><rect x="3" y="3" width="18" height="18" rx="4"/></svg> Resemblyzer Voice
                </span>
                <span style="font-weight: 700; color: #64748b; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="#64748b"><path d="M4 4h16v16H4z"/></svg> Streamlit Core
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 5. DEDICATED ROLE PORTALS
    st.markdown("""
        <section class="portals-section" id="portals" style="padding-top: 0;">
            <div class="portals-header">
                <span class="badge" style="margin-bottom: 16px;">⚡ Direct Access Portals</span>
                <h2>Choose Your Role</h2>
                <p>Select your dashboard to manage classroom sessions or enroll as a student.</p>
            </div>
        </section>
    """, unsafe_allow_html=True)

    p_col1, p_col2 = st.columns(2, gap="large")

    with p_col1:
        st.markdown("""
            <div class="portal-card teacher-card" style="box-shadow: none; border: none; padding: 0;">
                <div>
                    <div class="portal-header">
                        <div class="portal-icon teacher">👨‍🏫</div>
                        <div>
                            <div class="portal-tag teacher">Faculty & Instructors</div>
                            <div class="portal-title">Teacher Portal</div>
                        </div>
                    </div>
                    <p class="portal-desc">Create subjects, manage enrolled student rosters, batch analyze classroom attendance photos, and run voice speaker recognition.</p>
                    <ul class="portal-features">
                        <li><span class="check">✓</span> <span>AI Classroom Photo & Group Scan</span></li>
                        <li><span class="check">✓</span> <span>Voice Audio Speaker Identification</span></li>
                        <li><span class="check">✓</span> <span>Subject Management & Instant QR Codes</span></li>
                        <li><span class="check">✓</span> <span>Historical Attendance Logs & Analytics</span></li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Teacher Dashboard 👨‍🏫", type="primary", use_container_width=True, key="btn_portal_teacher"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with p_col2:
        st.markdown("""
            <div class="portal-card student-card" style="box-shadow: none; border: none; padding: 0;">
                <div>
                    <div class="portal-header">
                        <div class="portal-icon student">🎓</div>
                        <div>
                            <div class="portal-tag student">Students & Learners</div>
                            <div class="portal-title">Student Portal</div>
                        </div>
                    </div>
                    <p class="portal-desc">Enroll in subjects with one-click Join Codes or QR scans, register your facial biometrics and voice signature for instant attendance.</p>
                    <ul class="portal-features">
                        <li><span class="check">✓</span> <span>Biometric Face Login & Verification</span></li>
                        <li><span class="check">✓</span> <span>Instant Subject Join via Code or QR</span></li>
                        <li><span class="check">✓</span> <span>Personal Attendance Percentage & Logs</span></li>
                        <li><span class="check">✓</span> <span>Voice Profile & Audio Sample Enrollment</span></li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Student Dashboard 🎓", type="secondary", use_container_width=True, key="btn_portal_student"):
            st.session_state['login_type'] = 'student'
            st.rerun()

    # 6. FEATURES GRID
    st.markdown("""
        <section class="features" id="features">
            <h2>Built for High-Precision Classrooms</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="f-icon-box">⚡</div>
                    <h3>Multi-Face Attendance</h3>
                    <p>Recognize multiple students in a single classroom frame simultaneously within milliseconds using 128-d facial embeddings.</p>
                </div>
                <div class="feature-card">
                    <div class="f-icon-box">🎙️</div>
                    <h3>AI Voice Attendance</h3>
                    <p>Integrated Resemblyzer speaker recognition identifies speaking students directly from classroom audio clips.</p>
                </div>
                <div class="feature-card">
                    <div class="f-icon-box">📲</div>
                    <h3>Instant QR Auto-Enroll</h3>
                    <p>Generate unique subject join links and dynamic QR codes for rapid student onboarding into rosters.</p>
                </div>
                <div class="feature-card">
                    <div class="f-icon-box">📊</div>
                    <h3>Supabase Real-Time DB</h3>
                    <p>Cloud-native PostgreSQL database handles high-concurrency attendance logs and biometric vector indices.</p>
                </div>
                <div class="feature-card">
                    <div class="f-icon-box">🔒</div>
                    <h3>Encrypted Biometrics</h3>
                    <p>Student photos are converted into cryptographic mathematical vectors. Raw media is never exposed.</p>
                </div>
                <div class="feature-card">
                    <div class="f-icon-box">🌐</div>
                    <h3>Universal Hardware</h3>
                    <p>Works on standard laptops, webcams, classroom CCTV streams, or mobile camera uploads without extra sensors.</p>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # 7. TEACHER FLOW STEPS
    st.markdown("""
        <section class="teacher-flow" id="workflow">
            <div class="flow-container">
                <!-- Step 1 -->
                <div class="flow-step">
                    <div class="flow-content">
                        <span class="step-badge">STEP 01</span>
                        <h3>Subject Roster & QR Generation</h3>
                        <p>Teachers create subjects in seconds and share join codes or QR codes for seamless student registration and enrollment.</p>
                    </div>
                    <div class="flow-image">
                        <svg viewBox="0 0 600 360" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; display: block; background: #0f172a;">
                            <rect width="600" height="360" fill="#0b0f19"/>
                            <rect x="40" y="40" width="220" height="280" rx="16" fill="#182234" stroke="#334155"/>
                            <text x="150" y="80" font-family="'Outfit', sans-serif" font-size="14" fill="#ffffff" font-weight="700" text-anchor="middle">Subject: CS301 (AI)</text>
                            <rect x="75" y="105" width="150" height="150" rx="10" fill="#ffffff"/>
                            <rect x="90" y="120" width="40" height="40" fill="#000000"/>
                            <rect x="170" y="120" width="40" height="40" fill="#000000"/>
                            <rect x="90" y="200" width="40" height="40" fill="#000000"/>
                            <rect x="145" y="175" width="20" height="20" fill="#5865F2"/>
                            <text x="150" y="290" font-family="'Outfit', sans-serif" font-size="13" fill="#4BB786" font-weight="800" text-anchor="middle">CODE: AI-2026</text>

                            <rect x="290" y="40" width="270" height="280" rx="16" fill="#1e293b"/>
                            <text x="310" y="75" font-family="'Outfit', sans-serif" font-size="14" fill="#ffffff" font-weight="700">Enrolled Roster (48)</text>
                            
                            <rect x="310" y="95" width="230" height="40" rx="8" fill="#0f172a"/>
                            <circle cx="330" cy="115" r="12" fill="#5865F2"/>
                            <text x="352" y="120" font-family="'Outfit', sans-serif" font-size="12" fill="#e2e8f0" font-weight="600">Aarav Sharma</text>
                            <text x="520" y="120" font-family="'Outfit', sans-serif" font-size="10" fill="#4BB786" font-weight="700" text-anchor="end">READY</text>

                            <rect x="310" y="145" width="230" height="40" rx="8" fill="#0f172a"/>
                            <circle cx="330" cy="165" r="12" fill="#EB459E"/>
                            <text x="352" y="170" font-family="'Outfit', sans-serif" font-size="12" fill="#e2e8f0" font-weight="600">Priya Patel</text>
                            <text x="520" y="170" font-family="'Outfit', sans-serif" font-size="10" fill="#4BB786" font-weight="700" text-anchor="end">READY</text>

                            <rect x="310" y="250" width="230" height="45" rx="10" fill="#5865F2"/>
                            <text x="425" y="278" font-family="'Outfit', sans-serif" font-size="13" fill="#ffffff" font-weight="700" text-anchor="middle">Take Attendance 📸</text>
                        </svg>
                    </div>
                </div>

                <!-- Step 2 -->
                <div class="flow-step">
                    <div class="flow-image">
                        <svg viewBox="0 0 600 360" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; display: block; background: #0f172a;">
                            <rect width="600" height="360" fill="#0b0f19"/>
                            <rect x="40" y="30" width="520" height="50" rx="10" fill="#1e293b"/>
                            <text x="60" y="60" font-family="'Outfit', sans-serif" font-size="16" fill="#ffffff" font-weight="700">AI Facial & Voice Pipeline Active</text>
                            
                            <rect x="40" y="95" width="520" height="48" rx="8" fill="#182234"/>
                            <text x="60" y="125" font-family="'Outfit', sans-serif" font-size="13" fill="#cbd5e1" font-weight="600">01. Devansh Verma (Face Scan)</text>
                            <rect x="440" y="107" width="100" height="24" rx="12" fill="#4BB786" fill-opacity="0.2"/>
                            <text x="490" y="123" font-family="'Outfit', sans-serif" font-size="11" fill="#4BB786" font-weight="700" text-anchor="middle">PRESENT ✓</text>

                            <rect x="40" y="153" width="520" height="48" rx="8" fill="#182234"/>
                            <text x="60" y="183" font-family="'Outfit', sans-serif" font-size="13" fill="#cbd5e1" font-weight="600">02. Priya Sharma (Voice Print)</text>
                            <rect x="440" y="165" width="100" height="24" rx="12" fill="#4BB786" fill-opacity="0.2"/>
                            <text x="490" y="181" font-family="'Outfit', sans-serif" font-size="11" fill="#4BB786" font-weight="700" text-anchor="middle">PRESENT ✓</text>

                            <rect x="40" y="211" width="520" height="48" rx="8" fill="#182234"/>
                            <text x="60" y="241" font-family="'Outfit', sans-serif" font-size="13" fill="#cbd5e1" font-weight="600">03. Rohan Gupta (Face Scan)</text>
                            <rect x="440" y="223" width="100" height="24" rx="12" fill="#4BB786" fill-opacity="0.2"/>
                            <text x="490" y="239" font-family="'Outfit', sans-serif" font-size="11" fill="#4BB786" font-weight="700" text-anchor="middle">PRESENT ✓</text>
                        </svg>
                    </div>
                    <div class="flow-content">
                        <span class="step-badge">STEP 02</span>
                        <h3>Dual Biometric AI Identification</h3>
                        <p>Teachers can take a photo of the classroom or record a voice note. The machine learning pipeline extracts embeddings and matches registered students instantly.</p>
                    </div>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # 8. TECH STACK SECTION
    st.markdown("""
        <section class="tech-stack" id="tech">
            <span class="section-tag">ENGINEERED FOR BIOMETRIC SPEED & SCALE</span>
            <h2>Under The Hood</h2>
            <div class="tech-grid">
                <div class="tech-card">
                    <div class="t-icon">⚡</div>
                    <h4>Streamlit & Python</h4>
                    <p>Interactive dual-portal web architecture for teachers and students with zero latency state management.</p>
                    <span class="tech-tag">Frontend & Logic</span>
                </div>
                <div class="tech-card">
                    <div class="t-icon">👁️</div>
                    <h4>dlib & SVM Classifier</h4>
                    <p>128-dimensional facial embedding extractions with support vector machine classification for robust multi-face matching.</p>
                    <span class="tech-tag">Computer Vision</span>
                </div>
                <div class="tech-card">
                    <div class="t-icon">🎙️</div>
                    <h4>Resemblyzer & Librosa</h4>
                    <p>Deep voice embedding pipeline enabling speaker verification directly from classroom audio recordings.</p>
                    <span class="tech-tag">Voice Biometrics</span>
                </div>
                <div class="tech-card">
                    <div class="t-icon">🗄️</div>
                    <h4>Supabase (PostgreSQL)</h4>
                    <p>Scalable cloud database storing student profiles, biometric embeddings, subjects, and timestamped attendance logs.</p>
                    <span class="tech-tag">Cloud Database</span>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # 9. PURPLE CTA SECTION
    st.markdown("""
        <section class="purple-section" id="cta">
            <h2>Ready to Experience SMAPCLASS?</h2>
            <p>Experience the future of seamless AI attendance tracking and classroom management today.</p>
        </section>
    """, unsafe_allow_html=True)

    # 10. MAIN FOOTER
    st.markdown("""
        <footer class="main-footer" id="about">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div class="logo">
                        <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="SMAPCLASS Logo" style="height: 38px;">
                        <span class="logo-text">SMAPCLASS</span>
                    </div>
                    <p>AI-powered smart attendance system using biometric face and voice recognition pipelines.</p>
                </div>
                <div class="footer-links">
                    <h4>Direct Portals</h4>
                    <ul>
                        <li><a href="#portals">Teacher Dashboard</a></li>
                        <li><a href="#portals">Student Portal</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>System</h4>
                    <ul>
                        <li><a href="#features">Features</a></li>
                        <li><a href="#workflow">How It Works</a></li>
                        <li><a href="#tech">Tech Architecture</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Connected Endpoints</h4>
                    <ul>
                        <li><a href="https://github.com/abhinavrai2284/SMAPCLASS" target="_blank" rel="noopener">GitHub Repository</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 SMAPCLASS. Powered by Streamlit, Supabase, dlib & Resemblyzer AI.</p>
            </div>
        </footer>
    """, unsafe_allow_html=True)