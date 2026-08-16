"""
SMAPCLASS - Next-Gen AI Classroom Attendance Platform ⚡
Unified Application Launcher

Usage:
    python run.py
    streamlit run app.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent

def get_python_exe():
    """Finds the python executable in the local venv if present, else uses sys.executable."""
    venv_py_win = ROOT_DIR / "venv" / "Scripts" / "python.exe"
    venv_py_unix = ROOT_DIR / "venv" / "bin" / "python"
    if sys.platform == "win32" and venv_py_win.exists():
        return str(venv_py_win)
    elif venv_py_unix.exists():
        return str(venv_py_unix)
    return sys.executable

def main():
    py_exe = get_python_exe()
    port = int(os.getenv("PORT", 8501))

    print("\n" + "=" * 65)
    print("  🎓 SMAPCLASS - Next-Gen AI Classroom Attendance Platform")
    print("=" * 65)
    print(f"\n🚀 Launching SMAPCLASS All-in-One Engine on Port {port}...")
    print(f"👉 Local Access:   http://localhost:{port}")
    print("   (Press Ctrl+C to stop the service)\n" + "-" * 65 + "\n")

    cmd = [
        py_exe, "-m", "streamlit", "run", "app.py",
        "--server.port", str(port),
        "--server.headless", "true"
    ]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        proc = subprocess.Popen(cmd, cwd=str(ROOT_DIR), env=env)
        proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping SMAPCLASS gracefully...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        print("✅ SMAPCLASS stopped.")

if __name__ == "__main__":
    main()
