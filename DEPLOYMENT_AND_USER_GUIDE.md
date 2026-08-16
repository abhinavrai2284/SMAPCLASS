# 🎓 SMAPCLASS — Complete Deployment & User Manual

Welcome to **SMAPCLASS**, the enterprise-grade, AI-powered classroom attendance and engagement analytics platform. SMAPCLASS unifies 128-dimensional facial biometric recognition, voice speaker identification, dynamic QR auto-enrollment, and real-time database syncing into a single, high-performance web application.

---

## 📑 Table of Contents
1. [Platform Architecture & Core Technologies](#-platform-architecture--core-technologies)
2. [Local Setup & Development Guide](#-local-setup--development-guide)
3. [1-Click Streamlit Cloud Deployment Guide](#-1-click-streamlit-cloud-deployment-guide)
4. [Faculty / Teacher User Manual](#-faculty--teacher-user-manual)
5. [Student User Manual](#-student-user-manual)
6. [Database Schema & Secrets Setup](#-database-schema--secrets-setup)
7. [Troubleshooting & Frequently Asked Questions](#-troubleshooting--frequently-asked-questions)

---

## 🏛️ Platform Architecture & Core Technologies

SMAPCLASS runs as a unified **All-in-One Streamlit Application** that requires no secondary server processes:

```
                      ┌───────────────────────────────────────────────┐
                      │              SMAPCLASS App (app.py)           │
                      │  • Modern Landing Page & Quick Join Bar       │
                      │  • Teacher & Student Portal Switcher          │
                      └──────────────────────┬────────────────────────┘
                                             │
                   ┌─────────────────────────┴─────────────────────────┐
                   ▼                                                   ▼
       ┌──────────────────────┐                             ┌──────────────────────┐
       │   Faculty Portal     │                             │    Student Portal    │
       │ • Class Management   │                             │ • FaceID Enrollment  │
       │ • QR Generator       │                             │ • Voice Signature    │
       │ • Group Photo Scan   │                             │ • Subject Auto-Join  │
       │ • Voice Audio Recog  │                             │ • Attendance Metrics │
       │ • CSV Reports Export │                             │ • Real-Time Stats    │
       └──────────┬───────────┘                             └──────────┬───────────┘
                  │                                                    │
                  └─────────────────────────┬──────────────────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
     ┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
     │   dlib Face ML    │        │  Resemblyzer AI   │        │  Supabase Cloud   │
     │ 128-d Vectorizer  │        │ Speaker Embedder  │        │ Real-time Postgres│
     │ Haar / HOG Models │        │ Deep Voice Encoder│        │ Encrypted Vectors │
     └───────────────────┘        └───────────────────┘        └───────────────────┘
```

### Core Technologies
- **Frontend & App Framework**: [Streamlit](https://streamlit.io/) (with custom Google Fonts Outfit & Climate Crisis design system).
- **Facial Recognition**: `dlib` HOG Face Detector + 68-point Shape Predictor + ResNet 128-d Vectorizer.
- **Voice Recognition**: `Resemblyzer` (Deep learning voice encoder) + `librosa` audio processing.
- **Database & Storage**: `Supabase` (Cloud PostgreSQL with Row-Level Security & Real-Time Sync).
- **QR Engine**: `segno` for high-precision vector QR code generation.

---

## 💻 Local Setup & Development Guide

### Prerequisites
- **Python**: 3.10, 3.11, 3.12, or 3.13
- **Git**: Installed and configured
- **C++ Build Tools** (Optional for Windows; pre-compiled binaries are used by default)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/SMAPCLASS.git
cd SMAPCLASS
```

### 2. Create and Activate Virtual Environment
- **Windows (Command Prompt / PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root folder:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-or-service-key
```

### 5. Launch SMAPCLASS
- **Option A (1-Click on Windows)**: Double-click `start.bat`
- **Option B (Universal CLI)**:
  ```bash
  python run.py
  ```
- **Option C (Direct Streamlit)**:
  ```bash
  streamlit run app.py
  ```
Open your browser and navigate to **`http://localhost:8501`**.

---

## 🚀 1-Click Streamlit Cloud Deployment Guide

Deploying SMAPCLASS to **Streamlit Community Cloud** is completely automated via the included configuration files:

### Step 1: Push Code to GitHub
Ensure your repository is pushed to GitHub with:
- `app.py` (Main entrypoint)
- `requirements.txt` (Python dependencies)
- `packages.txt` (Linux C++/Audio dependencies for dlib & OpenCV)
- `.streamlit/config.toml` (Theme and server options)

### Step 2: Create App on Streamlit Cloud
1. Sign in to [share.streamlit.io](https://share.streamlit.io).
2. Click **"New app"**.
3. Select your repository: `username/SMAPCLASS`.
4. Branch: `main` (or default).
5. Main file path: `app.py`.

### Step 3: Configure Cloud Secrets
In the deployment dialog, click **"Advanced settings..."** > **Secrets** and paste:

```toml
SUPABASE_URL = "https://lddkomsesyexjwdtskfh.supabase.co"
SUPABASE_KEY = "sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"
```

*(Replace with your custom Supabase URL & Key if using your own instance).*

### Step 4: Click Deploy! ⚡
Streamlit Cloud will automatically:
1. Read `packages.txt` and install Linux binaries (`cmake`, `libopenblas-dev`, `libsndfile1`, `ffmpeg`, `libgl1`).
2. Read `requirements.txt` and install Python libraries.
3. Launch SMAPCLASS on a global public URL (e.g. `https://smapclass.streamlit.app`).

---

## 👨‍🏫 Faculty / Teacher User Manual

### 1. Teacher Registration & Login
1. On the Home page, click **"Open Teacher Dashboard 👨‍🏫"** (or append `?role=teacher` to the URL).
2. Enter your Teacher Username and Password, or click **"Register"** to create a new faculty account.

### 2. Subject Creation & QR Sharing
1. In the **"My Subjects"** tab, click **"Create Subject"**.
2. Provide:
   - **Subject Name** (e.g. *Artificial Intelligence & Machine Learning*)
   - **Subject Code** (e.g. *CS301*)
   - **Section / Batch** (e.g. *Section A*)
3. Click **"Create"**.
4. Click the **"Share / QR Code"** button on any subject card to view the dynamic QR code and copyable join code. Project this QR code onto the classroom screen for instant student onboarding.

### 3. Taking Multi-Face Group Attendance
1. Click on the **"Take Attendance"** tab.
2. Select the target Subject from the dropdown.
3. Upload a classroom wide-angle photo or capture directly from your webcam.
4. Click **"Process Attendance"**.
5. SMAPCLASS scans all faces simultaneously, matches them against enrolled student 128-d biometrics, logs timestamped attendance into Supabase, and displays marked Present/Absent student cards.

### 4. Taking Voice Attendance (Audio Identification)
1. In the **"Take Attendance"** tab, choose **"Voice Attendance"**.
2. Upload a lecture audio clip or discussion recording (`.wav` or `.mp3`).
3. Click **"Analyze Audio"**. The Resemblyzer AI engine splits audio into segments, matches speaker vectors against enrolled student voice profiles, and marks speaking students as Present.

### 5. Attendance History & CSV Export
1. Navigate to the **"Attendance Records"** tab.
2. Filter by Subject and Date.
3. View the live table of Present/Absent percentages.
4. Click **"Download CSV Report"** to export attendance rosters into Excel or your institution's LMS.

---

## 🎓 Student User Manual

### 1. Student Biometric Onboarding
1. On the Home page, click **"Open Student Portal 🎓"** (or append `?role=student` to the URL).
2. Click **"Register as New Student"**.
3. Fill in:
   - **Full Name** and **Roll Number / Student ID**.
   - **FaceID Enrollment**: Upload 3 to 5 clear facial photos with good lighting.
   - **Voice Signature**: Upload a short 5–10 second voice recording saying a sample sentence.
4. Click **"Complete Enrollment"**. SMAPCLASS computes mathematical vector descriptors and registers the student.

### 2. Joining Subjects via Join Code or QR Code
- **Method A (Landing Page Quick Join)**: Enter the Subject Code into the Quick Join bar on the homepage.
- **Method B (Inside Portal)**: Click **"Join Subject"**, type the Subject Code provided by your teacher, and click **"Enroll"**.
- **Method C (QR Code Scan)**: Scanning the teacher's QR code opens the link directly with `?role=student&join-code=<code>`.

### 3. Viewing Personal Attendance & Insights
- View your real-time attendance percentage per subject (e.g. *92% Present*).
- Review historical class logs, dates, and verification timestamps.

---

## 🗄️ Database Schema & Secrets Setup

SMAPCLASS utilizes 4 core relational tables in Supabase:

```sql
-- 1. Teachers Table
CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Students Table (with Vector Arrays)
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    face_embeddings JSONB,       -- Array of 128-d vectors
    voice_embedding JSONB,       -- Array of 256-d voice vector
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Subjects Table
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_code TEXT UNIQUE NOT NULL,
    subject_name TEXT NOT NULL,
    section TEXT,
    teacher_id UUID REFERENCES teachers(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Enrollments & Attendance Records
CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    subject_id UUID REFERENCES subjects(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID REFERENCES subjects(id),
    student_id UUID REFERENCES students(id),
    date DATE NOT NULL,
    time TIME NOT NULL,
    is_present BOOLEAN DEFAULT TRUE,
    verification_type TEXT,     -- 'face', 'voice', 'manual'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## ❓ Troubleshooting & Frequently Asked Questions

### 1. Face recognition reports "No faces detected"
- **Solution**: Ensure proper lighting and that faces are reasonably front-facing. The OpenCV Haar Cascade fallback automatically engages if dlib encounters low-contrast lighting.

### 2. Voice recognition threshold sensitivity
- **Solution**: The speaker verification similarity threshold is set to `0.65` by default in `src/pipelines/voice_pipeline.py`. For noisy lecture halls, adjust the `threshold` parameter between `0.55` and `0.70`.

### 3. Streamlit Cloud memory limits
- **Solution**: The dlib models and Resemblyzer encoders are wrapped in `@st.cache_resource`, ensuring they are loaded once into memory upon cold boot and shared across all user sessions without memory leaks.

---

<p align="center">
  <b>SMAPCLASS</b> • Automated Attendance & Classroom Intelligence<br>
  <i>Built with Streamlit, dlib, Resemblyzer & Supabase</i>
</p>
