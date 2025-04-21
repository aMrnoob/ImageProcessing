import io
from typing import Any
import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO
from ultralytics.utils import LOGGER
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.downloads import GITHUB_ASSETS_STEMS

class Inference:
    def __init__(self, **kwargs: Any):
        check_requirements("streamlit>=1.29.0")
        
        self.source = None
        self.enable_trk = False
        self.conf = 0.25
        self.iou = 0.45
        self.org_frame = None
        self.ann_frame = None
        self.vid_file_name = None
        self.selected_ind = []
        self.model = None

        self.temp_dict = {"model": None, **kwargs}
        self.model_path = self.temp_dict["model"]

        LOGGER.info(f"Ultralytics Solutions: ✅ {self.temp_dict}")

    def web_ui(self):
        menu_style_cfg = """<style>MainMenu {visibility: hidden;}</style>"""
        main_title_cfg = """<div><h1 style="color:#FF64DA; text-align:center; font-size:40px; margin-top:-50px;
        font-family: 'Archivo', sans-serif; margin-bottom:20px;">Ultralytics YOLO Streamlit Application</h1></div>"""
        sub_title_cfg = """<div><h4 style="color:#042AFF; text-align:center; font-family: 'Archivo', sans-serif; 
        margin-top:-15px; margin-bottom:50px;">Experience object detection with the power of Ultralytics YOLO! 🚀</h4></div>"""

        st.set_page_config(page_title="Ultralytics Streamlit App", layout="wide")
        st.markdown(menu_style_cfg, unsafe_allow_html=True)
        st.markdown(main_title_cfg, unsafe_allow_html=True)
        st.markdown(sub_title_cfg, unsafe_allow_html=True)

    def sidebar(self):
        with st.sidebar:
            logo = "https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg"
            st.image(logo, width=250)

        st.sidebar.title("User Configuration")
        self.source = st.sidebar.selectbox("Video Source", ("webcam", "video"))
        self.enable_trk = st.sidebar.radio("Enable Tracking", ("Yes", "No"), index=1)
        self.conf = float(st.sidebar.slider("Confidence Threshold", 0.0, 1.0, self.conf, 0.01))
        self.iou = float(st.sidebar.slider("IoU Threshold", 0.0, 1.0, self.iou, 0.01))

    def source_upload(self):
        self.vid_file_name = ""
        if self.source == "video":
            vid_file = st.sidebar.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv"])
            if vid_file is not None:
                g = io.BytesIO(vid_file.read())
                with open("ultralytics.mp4", "wb") as out:
                    out.write(g.read())
                self.vid_file_name = "ultralytics.mp4"
        elif self.source == "webcam":
            self.vid_file_name = 0

    def configure(self):
        available_models = [x.replace("yolo", "YOLO") for x in GITHUB_ASSETS_STEMS if x.startswith("yolo")]
        if self.model_path:
            available_models.insert(0, self.model_path.split(".pt")[0])

        selected_model = st.sidebar.selectbox("Model", available_models)

        with st.spinner("Loading model..."):
            self.model = YOLO(f"{selected_model.lower()}.pt")
            class_names = list(self.model.names.values())
        st.success("Model loaded successfully!")

        selected_classes = st.sidebar.multiselect("Classes", class_names, default=class_names[:3])
        if selected_classes:
            self.selected_ind = [class_names.index(option) for option in selected_classes]
        else:
            self.selected_ind = None  # Detect all if none selected

    def process_frame(self, img):
        """Process a single frame with YOLO model"""
        classes = self.selected_ind if self.selected_ind else None
        
        if self.enable_trk == "Yes":
            results = self.model.track(img, conf=self.conf, iou=self.iou, classes=classes, persist=True)
        else:
            results = self.model(img, conf=self.conf, iou=self.iou, classes=classes)
            
        return results[0].plot()

    def webcam_detection(self):
        """Handle webcam detection using Streamlit's camera_input"""
        st.warning("Note: Webcam detection processes one frame at a time. For real-time processing, please use our desktop application.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Original")
            picture = st.camera_input("Take a picture")
            
        with col2:
            st.header("Detection Results")
            if picture:
                img = cv2.imdecode(np.frombuffer(picture.getvalue(), np.uint8), cv2.IMREAD_COLOR)
                annotated_img = self.process_frame(img)
                st.image(annotated_img, channels="BGR", use_column_width=True)

    def video_detection(self):
        """Handle video file detection"""
        if self.vid_file_name:
            st.warning("Video processing is limited in this cloud version. For full video processing capabilities, please use our desktop application.")
            
            cap = cv2.VideoCapture(self.vid_file_name)
            if not cap.isOpened():
                st.error("Error opening video file")
                return
                
            frame_placeholder = st.empty()
            stop_button = st.button("Stop Processing")
            
            while cap.isOpened() and not stop_button:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                annotated_frame = self.process_frame(frame)
                frame_placeholder.image(annotated_frame, channels="BGR")
                
            cap.release()

    def inference(self):
        self.web_ui()
        self.sidebar()
        self.source_upload()
        self.configure()

        if self.source == "webcam":
            self.webcam_detection()
        elif self.source == "video":
            self.video_detection()


if __name__ == "__main__":
    import sys
    args = len(sys.argv)
    model = sys.argv[1] if args > 1 else None
    Inference(model=model).inference()
