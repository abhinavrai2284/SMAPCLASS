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


def parse_student_details(student):
    """Safely extracts clean display name and phone number from student record."""
    if not student:
        return {"name": "Unknown", "phone_number": "N/A"}
    raw_name = student.get('name', '')
    phone = student.get('phone_number') or student.get('phone') or ''
    
    if not phone and ' | ' in raw_name:
        parts = raw_name.split(' | ')
        clean_name = parts[0].strip()
        phone = parts[1].strip()
    else:
        clean_name = raw_name.strip()
        
    return {
        "name": clean_name,
        "phone_number": phone or "N/A"
    }


def get_all_students():
    if not supabase:
        return []
    try:
        response = supabase.table('students').select("*").execute()
        students = response.data or []
        for s in students:
            parsed = parse_student_details(s)
            s['clean_name'] = parsed['name']
            s['phone_number'] = parsed['phone_number']
        return students
    except Exception as e:
        print(f"Error get_all_students: {e}")
        return []


def create_student(new_name, face_embedding=None, voice_embedding=None, phone_number=None):
    if not supabase:
        return []
    clean_name = new_name.strip()
    clean_phone = phone_number.strip() if phone_number else ""
    
    # 1. Try inserting directly with phone_number column
    if clean_phone:
        try:
            data = {
                'name': clean_name,
                'phone_number': clean_phone,
                'face_embedding': face_embedding,
                'voice_embedding': voice_embedding
            }
            response = supabase.table('students').insert(data).execute()
            if response.data:
                return response.data
        except Exception:
            pass

    # 2. Resilient fallback: store phone formatted inside name field
    formatted_name = f"{clean_name} | {clean_phone}" if clean_phone else clean_name
    try:
        data = {
            'name': formatted_name,
            'face_embedding': face_embedding,
            'voice_embedding': voice_embedding
        }
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


def get_defaulter_students_for_teacher(teacher_id, threshold=75.0):
    """
    Identifies all enrolled students across teacher's subjects whose overall attendance is < threshold.
    Returns list of dicts with student details, subject name, attendance %, and phone number.
    """
    if not supabase:
        return []
    try:
        # 1. Fetch teacher subjects
        subjects = get_teacher_subjects(teacher_id)
        if not subjects:
            return []

        subject_map = {s['subject_id']: s for s in subjects}
        subject_ids = list(subject_map.keys())

        # 2. Fetch all enrolled students for these subjects
        enrolled_res = supabase.table('subject_students').select('*, students(*)').in_('subject_id', subject_ids).execute()
        enrolled_data = enrolled_res.data or []

        # 3. Fetch attendance logs for these subjects
        logs_res = supabase.table('attendance_logs').select('*').in_('subject_id', subject_ids).execute()
        logs_data = logs_res.data or []

        # Calculate sessions & attended count per (student_id, subject_id)
        sessions_per_subject = {}
        attended_per_student_subject = {}

        for log in logs_data:
            sub_id = log.get('subject_id')
            sid = log.get('student_id')
            ts = log.get('timestamp')
            is_present = bool(log.get('is_present', False))

            if sub_id not in sessions_per_subject:
                sessions_per_subject[sub_id] = set()
            if ts:
                sessions_per_subject[sub_id].add(ts)

            key = (sid, sub_id)
            if key not in attended_per_student_subject:
                attended_per_student_subject[key] = 0
            if is_present:
                attended_per_student_subject[key] += 1

        defaulters = []
        for item in enrolled_data:
            student = item.get('students')
            if not student:
                continue

            sid = student.get('student_id')
            sub_id = item.get('subject_id')
            sub_info = subject_map.get(sub_id, {})

            total_sessions = len(sessions_per_subject.get(sub_id, set()))
            # If classes have been taken
            if total_sessions > 0:
                attended_count = attended_per_student_subject.get((sid, sub_id), 0)
                pct = round((attended_count / total_sessions * 100), 1)

                if pct < threshold:
                    parsed = parse_student_details(student)
                    defaulters.append({
                        "student_id": sid,
                        "name": parsed["name"],
                        "phone_number": parsed["phone_number"],
                        "subject_id": sub_id,
                        "subject_name": sub_info.get('name', 'Unknown Subject'),
                        "subject_code": sub_info.get('subject_code', '-'),
                        "section": sub_info.get('section', '-'),
                        "total_classes": total_sessions,
                        "attended_classes": attended_count,
                        "missed_classes": total_sessions - attended_count,
                        "percentage": pct,
                    })

        return sorted(defaulters, key=lambda x: x['percentage'])
    except Exception as e:
        print(f"Error get_defaulter_students_for_teacher: {e}")
        return []
