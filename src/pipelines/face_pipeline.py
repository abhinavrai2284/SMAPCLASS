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
    """Loads dlib models if available, and OpenCV face cascade."""
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


def _compute_opencv_embedding(face_crop):
    """Computes a standardized 128-d vector embedding from a cropped face image."""
    try:
        resized = cv2.resize(face_crop, (64, 64))
        gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        
        # 1. 64-d Spatial block mean & std features
        blocks_mean = [np.mean(gray[r:r+8, c:c+8]) for r in range(0, 64, 8) for c in range(0, 64, 8)]
        # 2. 64-d Histogram features
        hist, _ = np.histogram(gray, bins=64, range=(0, 256), density=True)
        
        combined = np.concatenate([blocks_mean, hist])
        norm = np.linalg.norm(combined)
        if norm > 0:
            combined = combined / norm
        return combined
    except Exception as e:
        print(f"Error computing cv2 embedding: {e}")
        return np.zeros(128, dtype=np.float64)


def get_face_embeddings(image_input):
    """Extract 128-d face descriptors for all faces found in image."""
    detector, sp, facerec, face_cascade = load_dlib_models()

    try:
        image_np = _preprocess_image(image_input)
        if image_np is None or not isinstance(image_np, np.ndarray) or image_np.size == 0:
            return []

        # Mode A: dlib ResNet Pipeline (if dlib is installed)
        if detector and sp and facerec:
            faces = list(detector(image_np, 1))
            if len(faces) == 0:
                faces = list(detector(image_np, 0))
            if len(faces) == 0:
                faces = list(detector(image_np, 2))

            # Fallback to Haar Cascade if dlib detector misses
            if len(faces) == 0 and face_cascade is not None and cv2 is not None:
                gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
                gray_eq = cv2.equalizeHist(gray)
                cv_faces = face_cascade.detectMultiScale(gray_eq, scaleFactor=1.08, minNeighbors=3, minSize=(30, 30))
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
                    print(f"Error computing descriptor: {fe}")

            if encodings:
                return encodings

        # Mode B: OpenCV Fast Pipeline (when dlib is not available on Cloud)
        if face_cascade is not None and cv2 is not None:
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            gray_eq = cv2.equalizeHist(gray)
            cv_faces = face_cascade.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
            if len(cv_faces) == 0:
                cv_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=2, minSize=(25, 25))

            encodings = []
            h_img, w_img = image_np.shape[:2]
            for (x, y, w, h) in cv_faces:
                pad_w, pad_h = int(w * 0.1), int(h * 0.1)
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(w_img, x + w + pad_w)
                y2 = min(h_img, y + h + pad_h)
                crop = image_np[y1:y2, x1:x2]
                if crop.size > 0:
                    emb = _compute_opencv_embedding(crop)
                    encodings.append(emb)
            return encodings

        return []
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

    resemblance_threshold = 0.65

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
