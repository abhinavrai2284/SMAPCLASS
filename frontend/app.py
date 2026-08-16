import os
import sys
import urllib.request
from flask import Flask, render_template, redirect, request, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

STREAMLIT_URL = os.getenv('STREAMLIT_URL', 'http://localhost:8501')

@app.route('/')
def home():
    return render_template('index.html', streamlit_url=STREAMLIT_URL)

@app.route('/app')
def open_app():
    return redirect(STREAMLIT_URL)

@app.route('/teacher')
def teacher_portal():
    return redirect(f"{STREAMLIT_URL}")

@app.route('/student')
def student_portal():
    return redirect(f"{STREAMLIT_URL}")

@app.route('/join/<code_id>')
def join_subject(code_id):
    return redirect(f"{STREAMLIT_URL}/?join-code={code_id}")

@app.route('/embed')
def embed_view():
    return render_template('embed.html', streamlit_url=STREAMLIT_URL)

@app.route('/api/status')
def backend_status():
    is_online = False
    try:
        req = urllib.request.Request(STREAMLIT_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                is_online = True
    except Exception:
        is_online = False

    return jsonify({
        "status": "online" if is_online else "offline",
        "streamlit_url": STREAMLIT_URL,
        "message": "AI Attendance Engine Connected" if is_online else "Starting AI Engine..."
    })

if __name__ == '__main__':
    print("SMAPCLASS Web Server is running at: http://127.0.0.1:5000")
    print(f"Connected to SMAPCLASS Streamlit at: {STREAMLIT_URL}")
    app.run(host='127.0.0.1', port=5000, debug=True)
