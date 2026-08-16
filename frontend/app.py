import os
import sys
import urllib.request
from pathlib import Path
from flask import Flask, render_template, redirect, request, jsonify

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load environment variables from parent root or current directory
try:
    from dotenv import load_dotenv
    root_env = Path(__file__).resolve().parent.parent / '.env'
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, static_folder='static', template_folder='templates')

STREAMLIT_URL = os.getenv('STREAMLIT_URL', 'http://localhost:8501').rstrip('/')
FLASK_PORT = int(os.getenv('FLASK_PORT', os.getenv('PORT', 5000)))

@app.route('/')
def home():
    return render_template('index.html', streamlit_url=STREAMLIT_URL)

@app.route('/app')
def open_app():
    return redirect(STREAMLIT_URL)

@app.route('/teacher')
def teacher_portal():
    return redirect(f"{STREAMLIT_URL}/?role=teacher")

@app.route('/student')
def student_portal():
    return redirect(f"{STREAMLIT_URL}/?role=student")

@app.route('/join/<code_id>')
def join_subject(code_id):
    return redirect(f"{STREAMLIT_URL}/?role=student&join-code={code_id}")

@app.route('/embed')
def embed_view():
    return render_template('embed.html', streamlit_url=STREAMLIT_URL)

@app.route('/api/status')
def backend_status():
    is_online = False
    # Check Streamlit health endpoint or root URL
    endpoints = [f"{STREAMLIT_URL}/_stcore/health", STREAMLIT_URL]
    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (SMAPCLASS-HealthCheck)'})
            with urllib.request.urlopen(req, timeout=1.5) as response:
                if response.status in (200, 302, 304):
                    is_online = True
                    break
        except Exception:
            continue

    return jsonify({
        "status": "online" if is_online else "offline",
        "streamlit_url": STREAMLIT_URL,
        "message": "AI Attendance Engine Connected" if is_online else "Connecting to AI Engine on Port 8501..."
    })

if __name__ == '__main__':
    print("=" * 60)
    print(f"🚀 SMAPCLASS Landing Portal running at: http://127.0.0.1:{FLASK_PORT}")
    print(f"🔗 Connected AI Backend Streamlit URL: {STREAMLIT_URL}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)
