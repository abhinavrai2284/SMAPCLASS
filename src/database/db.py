import hashlib
import secrets
from src.database.config import supabase

try:
    import bcrypt
except ImportError:
    bcrypt = None


def hash_pass(pwd):
    if bcrypt:
        try:
            return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
        except Exception:
            pass
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + pwd).encode()).hexdigest()
    return f"sha256${salt}${hashed}"


def check_pass(pwd, hashed):
    if not hashed:
        return False
    if bcrypt and not str(hashed).startswith("sha256$"):
        try:
            return bcrypt.checkpw(pwd.encode(), str(hashed).encode())
        except Exception:
            pass
    if str(hashed).startswith("sha256$"):
        try:
            _, salt, h = str(hashed).split("$")
            return hashlib.sha256((salt + pwd).encode()).hexdigest() == h
        except Exception:
            return False
    return False


def check_teacher_exists(username):
    if not supabase:
        return False
    try:
        response = supabase.table("teachers").select("username").eq("username", username).execute()
        return len(response.data or []) > 0 
    except Exception as e:
        print(f"Error check_teacher_exists: {e}")
        return False


def create_teacher(username, password, name):
    if not supabase:
        return []
    try:
        data = { "username" : username, "password": hash_pass(password), "name": name}
        response = supabase.table("teachers").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error create_teacher: {e}")
        raise e


def teacher_login(username, password):
    if not supabase:
        return None
    try:
        response = supabase.table("teachers").select("*").eq("username", username).execute()
        if response.data:
            teacher = response.data[0]
            if check_pass(password, teacher.get('password', '')):
                return teacher
    except Exception as e:
        print(f"Error teacher_login: {e}")
    return None


def get_all_students():
    if not supabase:
        return []
    try:
        response = supabase.table('students').select("*").execute()
        return response.data or []
    except Exception as e:
        print(f"Error get_all_students: {e}")
        return []


def create_student(new_name, face_embedding=None, voice_embedding=None):
    if not supabase:
        return []
    try:
        data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
        response = supabase.table('students').insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error create_student: {e}")
        return []


def create_subject(subject_code, name, section, teacher_id):
    if not supabase:
        return []
    try:
        data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
        response = supabase.table("subjects").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error create_subject: {e}")
        raise e


def get_teacher_subjects(teacher_id):
    if not supabase:
        return []
    try:
        response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
        subjects = response.data or []

        for sub in subjects:
            sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
            attendance = sub.get('attendance_logs', [])
            unique_sessions = len(set(log['timestamp'] for log in attendance if isinstance(log, dict) and 'timestamp' in log))
            sub['total_classes'] = unique_sessions

            sub.pop('subject_students', None)
            sub.pop('attendance_logs', None)

        return subjects
    except Exception as e:
        print(f"Error get_teacher_subjects: {e}")
        return []


def enroll_student_to_subject(student_id, subject_id):
    if not supabase:
        return []
    try:
        data = {'student_id': student_id, "subject_id": subject_id}
        response = supabase.table('subject_students').insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error enroll_student_to_subject: {e}")
        return []


def unenroll_student_to_subject(student_id, subject_id):
    if not supabase:
        return []
    try:
        response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
        return response.data
    except Exception as e:
        print(f"Error unenroll_student_to_subject: {e}")
        return []


def get_student_subjects(student_id):
    if not supabase:
        return []
    try:
        response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data or []
    except Exception as e:
        print(f"Error get_student_subjects: {e}")
        return []


def get_student_attendance(student_id):
    if not supabase:
        return []
    try:
        response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
        return response.data or []
    except Exception as e:
        print(f"Error get_student_attendance: {e}")
        return []


def create_attendance(logs):
    if not supabase or not logs:
        return []
    try:
        response = supabase.table('attendance_logs').insert(logs).execute()
        return response.data
    except Exception as e:
        print(f"Error create_attendance: {e}")
        raise e


def get_attendance_for_teacher(teacher_id):
    if not supabase:
        return []
    try:
        response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
        return response.data or []
    except Exception as e:
        print(f"Error get_attendance_for_teacher: {e}")
        return []
