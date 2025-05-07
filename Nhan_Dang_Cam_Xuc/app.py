import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import ImageFont, ImageDraw, Image

def run():
    st.title("🎭 Nhận dạng cảm xúc")

    # Kiểm tra nếu mô hình chưa được tải vào session_state
    if 'is_load' not in st.session_state:
        # Tải mô hình nhận diện cảm xúc
        classifier = load_model(r"Nhan_Dang_Cam_Xuc\emotion_detection.h5")
        st.session_state.classifier = classifier

        # Định nghĩa các nhãn cảm xúc
        class_labels = ['Giận dữ', 'Ghê sợ', 'Sợ hãi', 'Hạnh phúc', 'Buồn', 'Bất ngờ', 'Bình thường']
        st.session_state.class_labels = class_labels

        # Cài đặt camera
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        st.session_state.face_classifier = face_classifier

        # Đánh dấu đã tải xong
        st.session_state.is_load = True

    # Bật/tắt camera
    camera_on = st.checkbox("Bật/Tắt Camera")
    if camera_on:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Không thể kết nối với camera. Vui lòng kiểm tra lại.")
            return

        stframe = st.empty()

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = st.session_state.face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    preds = st.session_state.classifier.predict(roi)[0]
                    label = st.session_state.class_labels[preds.argmax()]

                    # Vẽ văn bản lên hình
                    font = ImageFont.truetype("./arial.ttf", 20)
                    img_pil = Image.fromarray(frame)
                    draw = ImageDraw.Draw(img_pil)
                    text_position = (x, y - 40) if y - 40 > 0 else (x, y + h + 10)
                    draw.text(text_position, label, font=font, fill=(0, 255, 0))

                    frame = np.array(img_pil)

            stframe.image(frame, channels="BGR")

            # Thoát khi nhấn 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
