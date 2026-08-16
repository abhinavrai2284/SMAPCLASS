# SMAPCLASS ⚡🎓

**SMAPCLASS** is an AI-powered smart attendance and classroom management system built with Streamlit, Flask, Supabase, and cutting-edge biometric machine learning pipelines (Face Recognition with dlib/SVM and Voice Identification with Resemblyzer).

---

## 🌟 Key Features

- **Dual-Role Portals**: Dedicated interfaces for Teachers (Faculty) and Students.
- **Biometric Student Login & Registration**: Face-based login and optional voice enrollment.
- **Smart Teacher Attendance**:
  - **AI Classroom Photo Analysis**: Capture or batch-upload classroom photos to automatically detect and mark enrolled students present using 128-dimensional facial embedding vectors.
  - **AI Voice Attendance**: Analyze classroom audio recordings to identify speaking students via deep speaker embeddings.
- **Subject Management & Sharing**: Create subjects, manage rosters, and generate QR code/join links for instant student enrollment.
- **Integrated Frontend Landing Portal**: Modern, responsive landing page with quick join code input, role selection, and live backend health indicators located in `frontend/`.
- **Historical Attendance Records**: Aggregated attendance logs with timestamps and summary metrics.

---

## 🛠️ Architecture & Tech Stack

- **AI Attendance Backend**: [Streamlit](https://streamlit.io/) (v1.54+), `dlib`, `face_recognition_models`, `scikit-learn` (SVC), `resemblyzer`, `librosa`, `soundfile`.
- **Frontend Portal**: [Flask](https://flask.palletsprojects.com/) in `frontend/`, responsive HTML5/CSS3.
- **Database & Cloud**: [Supabase](https://supabase.com/) (PostgreSQL & Vector Storage).
- **QR Code Generation**: `segno`.
- **Containerization**: Docker & Docker Compose support.

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

### 3. Run the AI Attendance Backend (Streamlit)
```bash
streamlit run app.py --server.port 8501
```

### 4. Run the Modern Frontend Landing Page (Flask)
```bash
cd frontend
pip install -r requirements.txt
python app.py
```
Open **http://localhost:5000** in your browser to access the landing page and launch the integrated portals!

---

## 📦 Docker Deployment

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

---

## ⚙️ Heroku / Cloud PaaS

You can deploy to Heroku-like platforms using the `Procfile` included in the repo:

```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to GitHub (ensure `.streamlit/secrets.toml` is **not** committed).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app** and select:
   - **Repository**: `abhinavrai2284/SMAPCLASS`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Expand **Advanced settings** -> **Secrets** and configure `SUPABASE_URL` and `SUPABASE_KEY`.
5. Click **Deploy!**

> **Note**: `packages.txt` is pre-configured with Linux system packages (`cmake`, `libopenblas-dev`, `libsndfile1`, `ffmpeg`) needed for `dlib` and audio processing on Streamlit Cloud.

---

## 🔐 Secrets & Security

Never commit `secrets.toml` or your Supabase keys. Use your host's secret management (Streamlit Cloud secrets, Heroku Config Vars, or environment variables) to provide `SUPABASE_URL` and `SUPABASE_KEY`.

---

## 📄 License
MIT License © 2026 Abhinav Rai
