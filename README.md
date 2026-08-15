# SNAPCLASS 📸🎙️

**SNAPCLASS** is an AI-powered smart attendance system built with Streamlit, Supabase, and cutting-edge biometric machine learning pipelines (Face Recognition with dlib/SVM and Voice Identification with Resemblyzer).

---

## ✨ Features

- **Dual-Role Portals**: Dedicated interfaces for Teachers and Students.
- **Biometric Student Login & Registration**: Face-based login and optional voice enrollment.
- **Smart Teacher Attendance**:
  - **AI Classroom Photo Analysis**: Capture or batch-upload classroom photos to automatically detect and mark enrolled students present using 128-dimensional facial embedding vectors.
  - **AI Voice Attendance**: Analyze classroom audio recordings to identify speaking students via deep speaker embeddings.
- **Subject Management & Sharing**: Create subjects, manage rosters, and generate QR code/join links for instant student enrollment.
- **Historical Attendance Records**: Aggregated attendance logs with timestamps and summary metrics.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (v1.54+) with modern styling and responsive components.
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL & Auth).
- **Face Recognition**: `dlib`, `face_recognition_models`, `scikit-learn` (SVC).
- **Voice Recognition**: `resemblyzer`, `librosa`, `soundfile`.
- **QR Code Generation**: `segno`.

---

## 🚀 Getting Started (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/abhinavrai2284/SMAPCLASS.git
cd SMAPCLASS
```

### 2. Set up virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Supabase Secrets
Create `.streamlit/secrets.toml` in the root directory with your Supabase credentials:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
```

### 5. Run the application
```bash
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to GitHub (ensure `.streamlit/secrets.toml` is **not** committed).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app** and select:
   - **Repository**: `abhinavrai2284/SMAPCLASS`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Expand **Advanced settings** -> **Secrets** and paste:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
   ```
5. Click **Deploy!**

> **Note**: `packages.txt` is pre-configured with Linux system packages (`cmake`, `libopenblas-dev`, `libsndfile1`, `ffmpeg`) needed for `dlib` and audio processing on Streamlit Cloud.

## 📦 Docker (Container) Deployment

A Docker image is provided to run the app on any container platform (Cloud Run, ECS, DigitalOcean, etc.). Build and run locally:

```bash
# Build the image
docker build -t snapclass:latest .

# Run the container (exposes port 8501)
docker run -p 8501:8501 \
   -e SUPABASE_URL="https://your-project.supabase.co" \
   -e SUPABASE_KEY="your-supabase-key" \
   snapclass:latest
```

The container starts Streamlit on port 8501 by default. For platforms that provide a dynamic port, set the `PORT` environment variable; the Docker `CMD` supports `$PORT`.

## ⚙️ Heroku / Other PaaS

You can deploy to Heroku-like platforms using the `Procfile` included in the repo. Be sure to set `SUPABASE_URL` and `SUPABASE_KEY` as environment variables in the platform's dashboard. The `Procfile` runs:

```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## 🔐 Secrets

Never commit `secrets.toml` or your Supabase keys. Use your host's secret management (Streamlit Cloud secrets, Heroku Config Vars, or environment variables) to provide `SUPABASE_URL` and `SUPABASE_KEY`.
