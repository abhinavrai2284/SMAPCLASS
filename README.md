# SMAPCLASS ⚡🎓

**SMAPCLASS** is an AI-powered smart attendance and classroom management system built with Streamlit, Supabase, and cutting-edge biometric machine learning pipelines (Face Recognition with dlib/SVM and Voice Identification with Resemblyzer).

---

## 🌟 Key Features

- **Unified Single-App Architecture**: Rich landing page, Teacher Dashboard, and Student Portal all managed in a single entry point (`app.py`).
- **Dual-Role Portals**: Dedicated interfaces for Faculty (Teachers) and Students.
- **Biometric Student FaceID & Voice Enrollment**: Face-based login and optional voice enrollment in under 1 second.
- **Smart Teacher Attendance**:
  - **AI Classroom Photo Analysis**: Batch analyze classroom photos to detect and mark enrolled students present using 128-dimensional facial embedding vectors.
  - **AI Voice Attendance**: Analyze classroom audio recordings to identify speaking students via deep speaker embeddings.
- **Subject Management & Sharing**: Create subjects, manage rosters, and generate QR code/join links for instant student auto-enrollment.
- **Historical Attendance Records**: Aggregated attendance logs with timestamps and real-time metrics.

---

## 🛠️ Architecture & Tech Stack

- **Application Framework**: [Streamlit](https://streamlit.io/) (v1.54+)
- **Face Recognition AI**: `dlib`, `face_recognition_models`, `scikit-learn` (SVC)
- **Voice Recognition AI**: `resemblyzer`, `librosa`, `soundfile`
- **Database & Auth**: [Supabase](https://supabase.com/) (PostgreSQL & Vector Embeddings)
- **QR Code Engine**: `segno`
- **Containerization**: Docker (`Dockerfile`), Heroku/Render (`Procfile`)

---

## 🚀 Getting Started (Local Development)

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
```

### 3. Configure Supabase Credentials
Create `.streamlit/secrets.toml` or `.env` in the root directory:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
```

### 4. Run the Application
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser to access the complete application!

---

## ☁️ Deploying to Streamlit Cloud (Recommended)

1. Push your code to GitHub:
   ```bash
   git push origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and log in with your GitHub account.
3. Click **New app** and select:
   - **Repository**: `abhinavrai2284/SMAPCLASS`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Expand **Advanced settings** -> **Secrets** and paste your credentials:
   ```toml
   SUPABASE_URL = "https://lddkomsesyexjwdtskfh.supabase.co"
   SUPABASE_KEY = "sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"
   ```
5. Click **Deploy!**

> **Note**: `packages.txt` is pre-configured with Linux system packages (`cmake`, `libopenblas-dev`, `liblapack-dev`, `libsndfile1`, `ffmpeg`, `libgl1`) needed for `dlib` and audio processing on Streamlit Cloud.

---

## 📦 Docker Deployment

Build and run anywhere with Docker:

```bash
# 1. Build the Docker image
docker build -t smapclass:latest .

# 2. Run the container (exposing Port 8501)
docker run -p 8501:8501 \
   -e SUPABASE_URL="https://your-project.supabase.co" \
   -e SUPABASE_KEY="your-supabase-key" \
   smapclass:latest
```

---

## ⚙️ Heroku / Render / Cloud PaaS

Deploy to any PaaS using the included `Procfile`:
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 📄 License
MIT License © 2026 Abhinav Rai