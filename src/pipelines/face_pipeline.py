try:
    import dlib
    import face_recognition_models
except ImportError:
    dlib = None
    face_recognition_models = None

try:
    import cv2
except ImportError:
    cv2 = None

import io
import numpy as np
from PIL import Image
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    """Loads dlib frontal face detector, 68-point landmark shape predictor, and 128-d ResNet face recognizer."""
    detector = None
    sp = None
    facerec = None
    face_cascade = None

    if dlib is not None and face_recognition_models is not None:
        try:
            detector = dlib.get_frontal_face_detector()
            sp = dlib.shape_predictor(
                face_recognition_models.pose_predictor_model_location()
            )
            facerec = dlib.face_recognition_model_v1(
                face_recognition_models.face_recognition_model_location()
            )
        except Exception as e:
            print(f"Notice: dlib models could not be loaded: {e}")
            detector, sp, facerec = None, None, None

    if cv2 is not None:
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            if face_cascade.empty():
                face_cascade = None
        except Exception:
            face_cascade = None

    return detector, sp, facerec, face_cascade


def _preprocess_image(image_input):
    """Normalize any image input (PIL, RGBA, Grayscale, Float, Bytes) to uint8 8-bit RGB numpy array."""
    if isinstance(image_input, bytes):
        image_input = Image.open(io.BytesIO(image_input))

    if isinstance(image_input, Image.Image):
        image_input = np.array(image_input.convert('RGB'))
    elif isinstance(image_input, np.ndarray):
        if image_input.ndim == 2:
            image_input = np.stack([image_input] * 3, axis=-1)
        elif image_input.ndim == 3 and image_input.shape[2] == 4:
            image_input = image_input[:, :, :3]
        elif image_input.ndim == 3 and image_input.shape[2] == 1:
            image_input = np.concatenate([image_input] * 3, axis=-1)

        if image_input.dtype != np.uint8:
            if np.issubdtype(image_input.dtype, np.floating) and image_input.max() <= 1.0:
                image_input = (image_input * 255).astype(np.uint8)
            else:
                image_input = image_input.astype(np.uint8)

        image_input = np.ascontiguousarray(image_input)
    return image_input


def _rect_iou(r1, r2):
    """Computes Intersection-over-Union between two dlib rectangles."""
    left = max(r1.left(), r2.left())
    top = max(r1.top(), r2.top())
    right = min(r1.right(), r2.right())
    bottom = min(r1.bottom(), r2.bottom())

    if right <= left or bottom <= top:
        return 0.0

    intersection = (right - left) * (bottom - top)
    area1 = r1.width() * r1.height()
    area2 = r2.width() * r2.height()
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0.0


def _non_max_suppression_rects(rects, iou_thresh=0.35):
    """Suppresses duplicate bounding boxes for the same person across multi-scale detections."""
    if not rects:
        return []

    # Sort by area (larger bounding boxes first)
    sorted_rects = sorted(rects, key=lambda r: r.width() * r.height(), reverse=True)
    kept = []

    for r in sorted_rects:
        overlap = False
        for k in kept:
            if _rect_iou(r, k) > iou_thresh:
                overlap = True
                break
        if not overlap:
            kept.append(r)

    return kept


def get_face_embeddings(image_input):
    """
    Multi-Scale Deep Facial Descriptor Extractor.
    Scans for ALL students in individual and group classroom photos across multiple scales.
    Returns a list of 128-dimensional vector descriptors.
    """
    detector, sp, facerec, face_cascade = load_dlib_models()

    try:
        image_np = _preprocess_image(image_input)
        if image_np is None or not isinstance(image_np, np.ndarray) or image_np.size == 0:
            return []

        h_img, w_img = image_np.shape[:2]

        # ----------------------------------------------------
        # Mode A: dlib Deep ResNet Multi-Scale Detection
        # ----------------------------------------------------
        if detector and sp and facerec:
            all_raw_faces = []

            # 1. Scale 1: Standard detection for foreground faces
            faces_scale1 = list(detector(image_np, 1))
            all_raw_faces.extend(faces_scale1)

            # 2. Scale 0: Fast downscaled detection for very large / close-up faces
            faces_scale0 = list(detector(image_np, 0))
            all_raw_faces.extend(faces_scale0)

            # 3. Scale 2: Upsampled detection for background/smaller student faces in group photos
            # (Limit scale 2 to images <= 2000px on longest side to preserve memory)
            if max(h_img, w_img) <= 2000:
                faces_scale2 = list(detector(image_np, 2))
                all_raw_faces.extend(faces_scale2)

            # 4. Fallback/Augmentation: OpenCV Haar Cascade for side angles or challenging lighting
            if face_cascade is not None and cv2 is not None:
                gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
                gray_eq = cv2.equalizeHist(gray)
                cv_faces = face_cascade.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
                for (x, y, w, h) in cv_faces:
                    l = max(0, int(x))
                    t = max(0, int(y))
                    r = min(w_img, int(x + w))
                    b = min(h_img, int(y + h))
                    if r > l and b > t:
                        all_raw_faces.append(dlib.rectangle(l, t, r, b))

            # Deduplicate overlapping detections on the same student
            distinct_faces = _non_max_suppression_rects(all_raw_faces, iou_thresh=0.35)

            # Extract 128-d deep facial descriptor for EVERY student found in the group photo
            encodings = []
            for face in distinct_faces:
                try:
                    # Clip bounding box inside image boundaries
                    l = max(0, face.left())
                    t = max(0, face.top())
                    r = min(w_img, face.right())
                    b = min(h_img, face.bottom())
                    clipped_face = dlib.rectangle(l, t, r, b)

                    shape = sp(image_np, clipped_face)
                    descriptor = facerec.compute_face_descriptor(image_np, shape, num_jitters=1)
                    descriptor_arr = np.array(descriptor, dtype=np.float64)
                    encodings.append(descriptor_arr)
                except Exception as fe:
                    print(f"Error computing descriptor for student face: {fe}")

            return encodings

        # ----------------------------------------------------
        # Mode B: OpenCV Fast Multi-Scale Pipeline
        # ----------------------------------------------------
        if face_cascade is not None and cv2 is not None:
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            gray_eq = cv2.equalizeHist(gray)
            cv_faces = face_cascade.detectMultiScale(gray_eq, scaleFactor=1.08, minNeighbors=3, minSize=(25, 25))

            encodings = []
            for (x, y, w, h) in cv_faces:
                crop = image_np[max(0, y):min(h_img, y + h), max(0, x):min(w_img, x + w)]
                if crop.size > 0:
                    resized = cv2.resize(crop, (64, 64))
                    gray_crop = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
                    blocks_mean = [np.mean(gray_crop[r:r+8, c:c+8]) for r in range(0, 64, 8) for c in range(0, 64, 8)]
                    hist, _ = np.histogram(gray_crop, bins=64, range=(0, 256), density=True)
                    combined = np.concatenate([blocks_mean, hist])
                    norm = np.linalg.norm(combined)
                    if norm > 0:
                        combined = combined / norm
                    encodings.append(combined)

            return encodings

        return []
    except Exception as e:
        print(f"Error in get_face_embeddings: {e}")
        return []


@st.cache_resource
def get_trained_model():
    """Loads enrolled students and their 128-d facial embeddings from Supabase."""
    student_db = get_all_students()
    if not student_db:
        return None

    enrolled = []
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding and isinstance(embedding, list) and len(embedding) == 128:
            enrolled.append((student.get('student_id'), np.array(embedding, dtype=np.float64), student.get('name', '')))

    if not enrolled:
        return None

    return {'enrolled': enrolled}


def train_classifier():
    """Clears cached model resources to immediately refresh newly registered students."""
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    """
    Identifies all enrolled students present in classroom image (single or group).
    Returns (detected_students_dict, all_enrolled_ids_list, total_faces_detected_count).
    """
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    student_db = get_all_students()
    if not student_db:
        return detected_students, [], len(encodings)

    enrolled_students = []
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding and isinstance(embedding, list) and len(embedding) == 128:
            enrolled_students.append((student.get('student_id'), np.array(embedding, dtype=np.float64), student.get('name', '')))

    all_enrolled_ids = [s[0] for s in enrolled_students]
    if not enrolled_students:
        return detected_students, [], len(encodings)

    # 0.62 Euclidean distance threshold reliably matches faces while avoiding false positives
    resemblance_threshold = 0.62

    for encoding in encodings:
        best_match_id = None
        best_distance = float('inf')

        for sid, emb, sname in enrolled_students:
            dist = float(np.linalg.norm(emb - encoding))
            if dist < best_distance:
                best_distance = dist
                best_match_id = sid

        if best_match_id is not None and best_distance <= resemblance_threshold:
            detected_students[best_match_id] = True

    return detected_students, all_enrolled_ids, len(encodings)
