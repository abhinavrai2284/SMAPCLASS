import os
import json
import base64
from datetime import datetime
from pathlib import Path
from src.database.config import supabase

# Local persistent fallback directory
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
MATERIALS_FILE = DATA_DIR / "subject_materials.json"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not MATERIALS_FILE.exists():
        with open(MATERIALS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load_local_materials():
    _ensure_data_dir()
    try:
        with open(MATERIALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_local_materials(materials):
    _ensure_data_dir()
    try:
        with open(MATERIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving local materials: {e}")


def upload_subject_pdf(subject_id, teacher_id, title, filename, file_bytes):
    """
    Uploads a course PDF document for a specific subject.
    Stored in Supabase subject_materials and synced with persistent repository.
    """
    file_size_kb = f"{round(len(file_bytes) / 1024, 1)} KB" if len(file_bytes) < 1024 * 1024 else f"{round(len(file_bytes) / (1024 * 1024), 2)} MB"
    b64_data = base64.b64encode(file_bytes).decode("utf-8")
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    material_id = f"mat_{int(datetime.now().timestamp() * 1000)}"

    item = {
        "id": material_id,
        "subject_id": int(subject_id),
        "teacher_id": int(teacher_id) if teacher_id else None,
        "title": title.strip() if title else filename,
        "filename": filename,
        "file_size": file_size_kb,
        "file_data": b64_data,
        "uploaded_at": now_iso,
    }

    # 1. Try saving to Supabase subject_materials table
    if supabase:
        try:
            db_payload = {
                "subject_id": int(subject_id),
                "teacher_id": int(teacher_id) if teacher_id else None,
                "title": title.strip() if title else filename,
                "filename": filename,
                "file_size_kb": file_size_kb,
                "file_data": b64_data,
                "uploaded_at": now_iso,
            }
            res = supabase.table("subject_materials").insert(db_payload).execute()
            if res.data and len(res.data) > 0:
                item["id"] = res.data[0].get("id", material_id)
        except Exception as se:
            print(f"Supabase materials table notice: {se}")

    # 2. Save in local/cloud persistent store
    local_list = _load_local_materials()
    local_list.append(item)
    _save_local_materials(local_list)

    return item


def get_subject_materials(subject_id):
    """Fetches all active PDF materials uploaded for a specific subject."""
    subject_id = int(subject_id)

    # 1. Try querying Supabase
    if supabase:
        try:
            res = supabase.table("subject_materials").select("*").eq("subject_id", subject_id).order("uploaded_at", desc=True).execute()
            if res.data and len(res.data) > 0:
                results = []
                for row in res.data:
                    results.append({
                        "id": str(row.get("id")),
                        "subject_id": row.get("subject_id"),
                        "teacher_id": row.get("teacher_id"),
                        "title": row.get("title") or row.get("filename"),
                        "filename": row.get("filename"),
                        "file_size": row.get("file_size_kb") or "N/A",
                        "file_data": row.get("file_data"),
                        "uploaded_at": row.get("uploaded_at"),
                    })
                return results
        except Exception:
            pass

    # 2. Fallback to persistent local store
    local_list = _load_local_materials()
    matching = [m for m in local_list if m.get("subject_id") == subject_id]
    return sorted(matching, key=lambda x: x.get("uploaded_at", ""), reverse=True)


def delete_subject_pdf(material_id, subject_id=None):
    """
    Deletes a PDF material from the portal.
    Immediately deletes for both teacher and all enrolled students.
    """
    # 1. Try deleting from Supabase
    if supabase:
        try:
            # Try integer ID or string ID
            try:
                int_id = int(material_id)
                supabase.table("subject_materials").delete().eq("id", int_id).execute()
            except ValueError:
                supabase.table("subject_materials").delete().eq("id", material_id).execute()
        except Exception as se:
            print(f"Supabase delete notice: {se}")

    # 2. Delete from persistent local store
    local_list = _load_local_materials()
    filtered = [m for m in local_list if str(m.get("id")) != str(material_id)]
    _save_local_materials(filtered)
    return True


def get_student_course_materials(student_id):
    """
    Returns all uploaded PDF materials across all subjects the student is enrolled in.
    """
    from src.database.db import get_student_subjects
    enrolled = get_student_subjects(student_id)
    if not enrolled:
        return []

    materials_by_subject = []
    for node in enrolled:
        sub = node.get("subjects")
        if not sub:
            continue
        sub_id = sub.get("subject_id")
        mats = get_subject_materials(sub_id)
        for m in mats:
            m["subject_name"] = sub.get("name", "Subject")
            m["subject_code"] = sub.get("subject_code", "-")
            m["section"] = sub.get("section", "-")
            materials_by_subject.append(m)

    return sorted(materials_by_subject, key=lambda x: x.get("uploaded_at", ""), reverse=True)
