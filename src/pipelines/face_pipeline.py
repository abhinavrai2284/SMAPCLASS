

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

import numpy as np
from PIL import Image
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    if dlib is None or face_recognition_models is None:
        return None, None, None, None

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    face_cascade = None
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
    """Normalize any image input (PIL, RGBA, Grayscale, Float) to uint8 8-bit RGB numpy array."""
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


def get_face_embeddings(image_input):
    """Extract 128-d face descriptors for all faces found in image."""
    detector, sp, facerec, face_cascade = load_dlib_models()
    if not detector or not sp or not facerec:
        return []

    try:
        image_np = _preprocess_image(image_input)
        if image_np is None or not isinstance(image_np, np.ndarray) or image_np.size == 0:
            return []

        # 1. Try standard dlib HOG detector (upsample 1, then 0, then 2)
        faces = list(detector(image_np, 1))
        if len(faces) == 0:
            faces = list(detector(image_np, 0))
        if len(faces) == 0:
            faces = list(detector(image_np, 2))

        # 2. Fallback: OpenCV Haar Cascade detector with histogram equalization
        if len(faces) == 0 and face_cascade is not None and cv2 is not None:
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            # Equalize histogram for better detection in low/harsh lighting
            gray_eq = cv2.equalizeHist(gray)
            cv_faces = face_cascade.detectMultiScale(gray_eq, scaleFactor=1.08, minNeighbors=3, minSize=(30, 30))
            if len(cv_faces) == 0:
                cv_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

            h_img, w_img = image_np.shape[:2]
            for (x, y, w, h) in cv_faces:
                l = max(0, int(x))
                t = max(0, int(y))
                r = min(w_img, int(x + w))
                b = min(h_img, int(y + h))
                if r > l and b > t:
                    faces.append(dlib.rectangle(l, t, r, b))

        encodings = []
        for face in faces:
            try:
                shape = sp(image_np, face)
                face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
                encodings.append(np.array(face_descriptor, dtype=np.float64))
            except Exception as fe:
                print(f"Error computing descriptor for face: {fe}")

        return encodings
    except Exception as e:
        print(f"Error in get_face_embeddings: {e}")
        return []


@st.cache_resource
def get_trained_model():
    student_db = get_all_students()
    if not student_db:
        return None

    enrolled = []
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            enrolled.append((student.get('student_id'), np.array(embedding, dtype=np.float64)))

    if not enrolled:
        return None

    return {'enrolled': enrolled}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    student_db = get_all_students()
    if not student_db:
        return detected_student, [], len(encodings)

    enrolled_students = []
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            enrolled_students.append((student.get('student_id'), np.array(embedding, dtype=np.float64)))

    all_students = [s[0] for s in enrolled_students]
    if not enrolled_students:
        return detected_student, [], len(encodings)

    resemblance_threshold = 0.65  # Accommodates webcam lighting & resolution differences reliably

    for encoding in encodings:
        best_match_id = None
        best_distance = float('inf')

        for sid, emb in enrolled_students:
            dist = float(np.linalg.norm(emb - encoding))
            if dist < best_distance:
                best_distance = dist
                best_match_id = sid

        if best_match_id is not None and best_distance <= resemblance_threshold:
            detected_student[best_match_id] = True

    return detected_student, all_students, len(encodings)

