import streamlit as st
import cv2
import numpy as np
import pickle
import os

def run():
    st.title("🎭 Nhận dạng khuôn mặt")

    detection_model = "C:/Users/Admin/Documents/Github/ImageProcessing/ImageProcessing/Nhan_Dang_Khuon_Mat/model/face_detection_yunet_2023mar.onnx"
    recognition_model = "C:/Users/Admin/Documents/Github/ImageProcessing/ImageProcessing/Nhan_Dang_Khuon_Mat/model/face_recognition_sface_2021dec.onnx"
    database_path = "C:/Users/Admin/Documents/Github/ImageProcessing/ImageProcessing/Nhan_Dang_Khuon_Mat/model/svc.pkl"

    detector = cv2.FaceDetectorYN.create(
        detection_model,
        "",
        (320, 320),
        0.9, 
        0.3,  
        5000  
    )

    recognizer = cv2.FaceRecognizerSF.create(
        recognition_model,
        ""
    )

    if os.path.exists(database_path):
        with open(database_path, 'rb') as f:
            avg_reference = pickle.load(f)
    else:
        st.error("❌ Không tìm thấy database, vui lòng tạo database trước.")
        return

    st.warning("📷 Nhấn 'Start Camera' để nhận diện khuôn mặt từ webcam. Dừng bằng nút 'Stop'.")

    start = st.button("Start Camera")
    stop = st.button("Stop")

    if start:
        cap = cv2.VideoCapture(0)
        frame_placeholder = st.empty()

        if not cap.isOpened():
            st.error("❌ Không mở được webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]
            detector.setInputSize((w, h))
            _, faces = detector.detect(frame)

            if faces is not None:
                for face in faces:
                    aligned_face = recognizer.alignCrop(frame, face)
                    query_embedding = recognizer.feature(aligned_face)

                    max_score = 0
                    best_match = "Unknown"
                    for ref_name, ref_embedding in avg_reference.items():
                        score = recognizer.match(query_embedding, ref_embedding, cv2.FaceRecognizerSF_FR_COSINE)
                        if score > max_score:
                            max_score = score
                            if score > 0.5:
                                best_match = ref_name

                    box = list(map(int, face[:4]))
                    cv2.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
                    cv2.putText(frame, f"{best_match} ({max_score:.2f})", (box[0], box[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB")

            if stop:
                break

        cap.release()
