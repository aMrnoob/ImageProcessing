import streamlit as st
from PIL import Image
import numpy as np
import os
import cv2
from face_recognition_app.utils import load_known_faces, recognize_faces, recognize_faces_video

FACE_DIR = "face_recognition_app/faces_recognized"

def run():
    os.makedirs(FACE_DIR, exist_ok=True)
    known_faces = load_known_faces(FACE_DIR)
    st.header("🎭 Nhận diện khuôn mặt")
    tab1, tab2, tab3 = st.tabs(["➕ Đăng ký khuôn mặt mới", "🔍 Nhận diện khuôn mặt", "📹 Nhận diện từ video"])

    with tab1:
        with st.form(key="register_form"):
            name_input = st.text_input("👤 Nhập tên người")
            upload_face = st.file_uploader("📥 Tải ảnh chân dung", type=["jpg", "jpeg", "png"], key="face_uploader")
            submit_button = st.form_submit_button("💾 Lưu khuôn mặt")

            if submit_button and upload_face and name_input.strip():
                img = Image.open(upload_face).convert("RGB")
                img_np = np.array(img)
                img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                filename = os.path.join(FACE_DIR, f"{name_input.strip().lower()}.jpg")
                cv2.imwrite(filename, img_bgr)

                st.success(f"✅ Đã lưu khuôn mặt cho {name_input}")
                st.rerun()

    with tab2:
        uploaded_image = st.file_uploader("📤 Tải ảnh có nhiều khuôn mặt", type=["jpg", "jpeg", "png"], key="detect_uploader")
        if uploaded_image:
            img = Image.open(uploaded_image).convert("RGB")
            img_np = np.array(img)
            recognized_img = recognize_faces(img_np, known_faces)
            st.image(cv2.cvtColor(recognized_img, cv2.COLOR_BGR2RGB), caption="📸 Kết quả nhận diện", use_column_width=True)

    with tab3:
        st.subheader("🎥 Nhận diện từ video")
        option = st.radio("Chọn nguồn video:", ("📁 Tải lên video", "📷 Dùng webcam"))
        known_faces = load_known_faces()

        if option == "📁 Tải lên video":
            video_file = st.file_uploader("📤 Tải video (MP4, AVI...)", type=["mp4", "avi", "mov"])
            if video_file:
                tpath = f"temp_video_{video_file.name}"
                with open(tpath, "wb") as f:
                    f.write(video_file.read())
                recognize_faces_video(tpath, known_faces)

        elif option == "📷 Dùng webcam":
            run_webcam_recognition(known_faces)

def run_webcam_recognition(known_faces):
    cap = cv2.VideoCapture(0) 

    stframe = st.empty()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (800, 600))
        annotated = recognize_faces(frame, known_faces)
        stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)

    cap.release()

