# SMAPCLASS-FRONTEND ⚡

> **Next-Gen AI Classroom Attendance & Analytics Platform**

SMAPCLASS-FRONTEND is a modern, responsive web application and landing portal for **SMAPCLASS** — an AI-powered smart attendance system featuring real-time facial recognition, speaker voice identification, and automated classroom analytics.

---

## ✨ Key Features

- **🎯 Role-Based Portals**: Direct quick-launch interfaces for Teachers (Faculty) and Students.
- **⚡ Quick Join System**: In-page subject join code launcher with auto-enrollment integration.
- **🖥️ In-Page Live App Modal**: Embedded application frame for testing and live demonstrations.
- **🟢 Live Backend Health Indicator**: Real-time polling to detect the AI engine status on Port 8501.
- **📱 Fully Responsive Design**: Mobile, tablet, and desktop optimized glassmorphic layout.

---

## 🛠️ Tech Stack

- **Backend / Router**: Python & [Flask](https://flask.palletsprojects.com/)
- **Frontend Styling**: Modern CSS3, Glassmorphism, Google Fonts (`Climate Crisis`, `Outfit`)
- **Connected AI Backend**: Streamlit, Supabase, `dlib`, `Resemblyzer`, `PyTorch`

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/abhinavrai2284/SMAPCLASS-FRONTEND.git
cd SMAPCLASS-FRONTEND
```

### 2. Set up virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

---

## 🔗 Connecting with SMAPCLASS Backend

To connect with the live AI engine:
1. Start the main **SMAPCLASS** backend:
   ```bash
   streamlit run app.py --server.port 8501
   ```
2. The frontend automatically connects to `http://localhost:8501` and displays the live engine status.

---

## 📄 License
MIT License © 2026 Abhinav Rai
