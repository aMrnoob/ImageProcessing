from ultralytics import YOLO
import streamlit as st
from PIL import Image
import numpy as np
import cv2

def run():
    st.header("🍎 Nhận dạng đối tượng bằng YOLOv8")

    model_path = "Nhan_Dang_Doi_Tuong/model/yolov8n.pt"
    model = YOLO(model_path)

    image_file = st.file_uploader("📷 Upload ảnh", type=["bmp", "png", "jpg", "jpeg"])

    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Ảnh gốc")
        frame = np.array(image)

        if st.button("🔍 Nhận dạng"):
            results = model.predict(source=frame, conf=0.5)

            annotated = frame.copy()
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()

                for box, conf, cls_id in zip(boxes, confs, classes):
                    x1, y1, x2, y2 = map(int, box)
                    label = f"{model.names[int(cls_id)]} {conf:.2f}"
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            st.image(annotated, caption="Kết quả", channels="RGB")
