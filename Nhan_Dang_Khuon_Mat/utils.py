import os
import numpy as np
import cv2
import onnxruntime as ort
from numpy.linalg import norm
from Nhan_Dang_Khuon_Mat.yunet import YuNet
import streamlit as st

detector = YuNet(
    modelPath="Nhan_Dang_Khuon_Mat/model/face_detection_yunet_2023mar.onnx",
    inputSize=[640, 640],
    confThreshold=0.6,
    nmsThreshold=0.3,
    topK=5000,
    backendId=cv2.dnn.DNN_BACKEND_DEFAULT,
    targetId=cv2.dnn.DNN_TARGET_CPU
)
recognizer = ort.InferenceSession("Nhan_Dang_Khuon_Mat/model/face_recognition_sface_2021dec.onnx")

def detect_faces(img, conf_thresh=0.9):
    h, w = img.shape[:2]
    detector.setInputSize([w, h])
    results = detector.infer(img)
    boxes = []

    if results is not None:
        for x, y, w_box, h_box, *_, conf in results:
            if conf >= conf_thresh:
                boxes.append([int(x), int(y), int(x + w_box), int(y + h_box)])
    
    return boxes

def load_known_faces(folder="Nhan_Dang_Khuon_Mat/faces_recognized"):
    known = {}
    for file in os.listdir(folder):
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')): continue
        name = os.path.splitext(file)[0]
        img = cv2.imread(os.path.join(folder, file))
        if img is None: continue

        boxes = detect_faces(img)
        if len(boxes) != 1:
            continue

        face_tensor = preprocess_face(img, boxes[0])
        if face_tensor is not None:
            known[name] = get_embedding(face_tensor)

    return known

def recognize_faces(img, known_faces, threshold=0.4):
    boxes = detect_faces(img)
    annotated = img.copy()

    for box in boxes:
        face_tensor = preprocess_face(img, box)
        if face_tensor is None:
            continue
        emb = get_embedding(face_tensor)
        best_match = "Unknown"
        best_dist = float("inf")
        for name, known_emb in known_faces.items():
            dist = np.linalg.norm(emb - known_emb)
            if dist < best_dist:
                base_name = name.rsplit('_', 1)[0]
                best_match = base_name
                best_dist = dist

        label = f"{best_match} ({best_dist:.2f})" if best_dist < threshold else f"Unknown ({best_dist:.2f})"
        color = (0, 255, 0) if best_dist < threshold else (0, 0, 255)

        x1, y1, x2, y2 = box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
    return annotated

def preprocess_face(img, box):
    x1, y1, x2, y2 = box
    face = img[y1:y2, x1:x2]
    if face.size == 0: return None
    face = cv2.resize(face, (112, 112))
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return np.transpose(face, (2, 0, 1))[np.newaxis, :]

def get_embedding(face_tensor):
    input_name = recognizer.get_inputs()[0].name
    emb = recognizer.run(None, {input_name: face_tensor})[0][0]
    return emb / norm(emb)

def recognize_faces_video(video_path, known_faces):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Không thể mở video.")
        return

    stframe = st.empty()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        annotated = recognize_faces(frame, known_faces)
        stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    
    cap.release()