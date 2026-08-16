import streamlit as st
import streamlit.components.v1 as components
import os

def home_screen():
    # Hide Streamlit Default UI chrome for clean fullscreen landing experience
    st.markdown("""
        <style>
        #MainMenu, footer, header {
            visibility: hidden !important;
            display: none !important;
        }
        .stApp {
            background-color: #fcfcfd !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Read the exact styles.css
    base_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_dir, "..", "..", "frontend", "static", "img", "css", "styles.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(base_dir, "..", "..", "frontend", "static", "css", "styles.css")

    css_code = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()

    # Self-contained HTML with the EXACT same markup and styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SMAPCLASS - Next-Gen AI Classroom Attendance & Analytics</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
        {css_code}
        
        /* Full width and seamless adjustments */
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            overflow-x: hidden;
            background-color: #fcfcfd;
        }}
        .navbar {{
            padding: 14px 60px;
        }}
        .hero {{
            padding: 100px 40px 80px;
            background-color: #f0f4ff;
        }}
        </style>
    </head>
    <body>

        <!-- Navigation Bar -->
        <header class="navbar">
            <div class="logo">
                <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="SMAPCLASS Logo" onerror="this.style.display='none'">
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
                <div class="status-pill" title="AI Biometric Attendance Engine">
                    <span class="status-dot online"></span>
                    <span>AI Engine: Online (8501)</span>
                </div>
                <button onclick="navigateTo('teacher')" class="btn-pill" style="border: none; cursor: pointer;">
                    Launch App ⚡
                </button>
            </div>
        </header>

        <!-- Hero Section -->
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
            
            <!-- Quick Join Form -->
            <form class="join-container" onsubmit="handleQuickJoin(event)">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <input type="text" id="quickJoinInput" class="join-input" placeholder="Enter Subject Join Code (e.g. CS301)..." required autocomplete="off">
                <button type="submit" class="join-btn">
                    Join Class
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
            </form>

            <div class="hero-actions">
                <button onclick="navigateTo('teacher')" class="btn-cta" style="border: none; cursor: pointer;">
                    <span>👨‍🏫</span> Faculty Dashboard
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
                <button onclick="navigateTo('student')" class="btn-cta" style="border: none; cursor: pointer; background: #1e1e2f;">
                    <span>🎓</span> Student FaceID Login
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
            </div>

            <div class="integrated">
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
        </section>

        <!-- Role Portals Section -->
        <section class="portals-section" id="portals">
            <div class="portals-header">
                <span class="badge" style="margin-bottom: 16px;">⚡ Direct Access Portals</span>
                <h2>Choose Your Role</h2>
                <p>Select your dashboard to manage classroom sessions or enroll as a student.</p>
            </div>

            <div class="portals-grid">
                <!-- Teacher Card -->
                <div class="portal-card teacher-card">
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
                    <div class="portal-actions-row">
                        <button onclick="navigateTo('teacher')" class="portal-btn primary" style="width: 100%;">
                            Open Teacher Dashboard 👨‍🏫
                        </button>
                    </div>
                </div>

                <!-- Student Card -->
                <div class="portal-card student-card">
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
                    <div class="portal-actions-row">
                        <button onclick="navigateTo('student')" class="portal-btn primary" style="width: 100%; background: #1e1e2f;">
                            Open Student Dashboard 🎓
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
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

        <!-- Teacher Flow Section -->
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

                            <rect x="310" y="195" width="230" height="40" rx="8" fill="#0f172a"/>
                            <circle cx="330" cy="215" r="12" fill="#3b82f6"/>
                            <text x="352" y="220" font-family="'Outfit', sans-serif" font-size="12" fill="#e2e8f0" font-weight="600">Rohan Verma</text>
                            <text x="520" y="220" font-family="'Outfit', sans-serif" font-size="10" fill="#4BB786" font-weight="700" text-anchor="end">READY</text>

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

        <!-- Tech Stack Section -->
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

        <!-- Purple CTA Section -->
        <section class="purple-section" id="cta">
            <h2>Ready to Experience SMAPCLASS?</h2>
            <p>Experience the future of seamless AI attendance tracking and classroom management today.</p>
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
                <button onclick="navigateTo('teacher')" class="btn-white" style="border: none; cursor: pointer;">
                    Launch Faculty Dashboard 👨‍🏫
                </button>
                <button onclick="navigateTo('student')" class="btn-white" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid white; cursor: pointer;">
                    Launch Student Portal 🎓
                </button>
            </div>
        </section>

        <!-- Main Footer -->
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
                        <li><a href="javascript:void(0)" onclick="navigateTo('teacher')">Teacher Dashboard</a></li>
                        <li><a href="javascript:void(0)" onclick="navigateTo('student')">Student Portal</a></li>
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

        <!-- Javascript Navigation Bridge to Streamlit -->
        <script>
            function navigateTo(role) {{
                try {{
                    window.parent.location.search = '?role=' + role;
                }} catch (e) {{
                    window.location.search = '?role=' + role;
                }}
            }}

            function handleQuickJoin(event) {{
                event.preventDefault();
                var code = document.getElementById('quickJoinInput').value.trim();
                if (code) {{
                    try {{
                        window.parent.location.search = '?role=student&join-code=' + encodeURIComponent(code);
                    }} catch (e) {{
                        window.location.search = '?role=student&join-code=' + encodeURIComponent(code);
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """

    # Render 100% pixel-for-pixel exact full HTML page
    components.html(html_content, height=3100, scrolling=False)