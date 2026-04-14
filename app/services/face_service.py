import cv2
import numpy as np
import os

# ✅ Updated paths for deployment
DATASET_PATH = "app/dataset"
MODEL_PATH = "app/face_model.yml"

recognizer = cv2.face.LBPHFaceRecognizer_create()


def train_model():
    faces = []
    labels = []
    label_map = {}
    current_label = 0

    # ✅ Safety check
    if not os.path.exists(DATASET_PATH):
        return {}

    for person_name in os.listdir(DATASET_PATH):
        person_path = os.path.join(DATASET_PATH, person_name)

        if not os.path.isdir(person_path):
            continue

        label_map[current_label] = person_name

        for image_name in os.listdir(person_path):
            img_path = os.path.join(person_path, image_name)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    # ✅ No data case
    if len(faces) == 0:
        return {}

    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)

    return label_map


def recognize_face(image, label_map):
    import os

    # ✅ Model file check
    if not os.path.exists(MODEL_PATH):
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    recognizer.read(MODEL_PATH)

    label, confidence = recognizer.predict(gray)

    # ✅ Tuned threshold
    if confidence < 70:
        return label_map.get(label)

    return None