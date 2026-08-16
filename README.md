# 🎓 SMAPCLASS ⚡
> **Next-Gen AI Biometric Attendance & Classroom Analytics Platform**

SMAPCLASS is an enterprise-ready, all-in-one AI classroom attendance system built with Streamlit, Supabase, and cutting-edge biometric machine learning pipelines:
- ⚡ **128-d Facial Recognition** (`dlib`, `face_recognition_models`, `scikit-learn` SVC)
- 🎙️ **Deep Voice Speaker Identification** (`Resemblyzer`, `librosa`, `soundfile`)
- 📲 **Dynamic QR Auto-Enrollment** (`segno`)
- 📊 **Real-Time Cloud Database** ([Supabase](https://supabase.com/))

---

## 🌟 Key Capabilities

- **Unified All-in-One Single-App Architecture**: Rich modern landing page, quick join code bar, Teacher Dashboard, and Student Portal all managed in a single entry point (`app.py`).
- **Dual-Role Portals**: Dedicated interfaces for Faculty (Teachers) and Students with 1-click navigation.
- **Biometric Student FaceID & Voice Enrollment**: Sub-second face-based login, biometric vector registration, and voice signature enrollment.
- **Smart Faculty Attendance**:
  - **AI Classroom Photo Analysis**: Batch analyze classroom group photos to detect and mark enrolled students present in milliseconds.
  - **AI Voice Attendance**: Analyze lecture audio recordings to identify speaking students via deep speaker embeddings.
- **Subject Management & Sharing**: Create subjects, manage rosters, and generate dynamic QR codes and copyable join links for instant student auto-enrollment.
- **Historical Attendance Records**: Aggregated attendance logs with timestamps, percentages, and one-click CSV export.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/abhinavrai2284/SMAPCLASS.git
cd SMAPCLASS
```

### 2. Set up virtual environment & install dependencies
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Supabase Credentials
Create `.env` (or `.streamlit/secrets.toml`) in the root directory:
```env
SUPABASE_URL="https://lddkomsesyexjwdtskfh.supabase.co"
SUPABASE_KEY="sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"
```

### 4. Run the Application
- **Windows 1-Click**: Double-click `start.bat`
- **CLI**:
  ```bash
  python run.py
  # OR
  streamlit run app.py
  ```
Open **`http://localhost:8501`** in your browser!

---

## ☁️ 1-Click Streamlit Cloud Deployment

1. Push your repository to GitHub:
   ```bash
   git push origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and log in with GitHub.
3. Click **New app** and select:
   - **Repository**: `abhinavrai2284/SMAPCLASS`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Expand **Advanced settings** -> **Secrets** and paste:
   ```toml
   SUPABASE_URL = "https://lddkomsesyexjwdtskfh.supabase.co"
   SUPABASE_KEY = "sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"
   ```
5. Click **Deploy!** 🚀

> **Note**: `packages.txt` is pre-configured with Linux system packages (`cmake`, `libopenblas-dev`, `liblapack-dev`, `libsndfile1`, `ffmpeg`, `libgl1`) needed for `dlib` and audio processing on Streamlit Cloud.

---

## 📖 Complete Manual & Documentation

For comprehensive step-by-step instructions, database schemas, teacher/student user manuals, and troubleshooting, read the **[DEPLOYMENT_AND_USER_GUIDE.md](DEPLOYMENT_AND_USER_GUIDE.md)**.

---

## 📄 License
MIT License © 2026 Abhinav Rai