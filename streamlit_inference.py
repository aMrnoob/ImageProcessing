import io
from typing import Any
import av
from ultralytics import YOLO
from ultralytics.utils import LOGGER
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.downloads import GITHUB_ASSETS_STEMS
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase


class Inference:

    def __init__(self, **kwargs: Any):
        check_requirements("streamlit>=1.29.0")
        import streamlit as st
        self.st = st

        self.enable_trk = False
        self.conf = 0.25
        self.iou = 0.45
        self.model = None
        self.selected_ind = []

        self.temp_dict = {"model": None, **kwargs}
        self.model_path = self.temp_dict["model"]
        LOGGER.info(f"Ultralytics Solutions: ✅ {self.temp_dict}")

    def web_ui(self):
        menu_style_cfg = """<style>MainMenu {visibility: hidden;}</style>"""
        main_title_cfg = """<div><h1 style="color:#FF64DA; text-align:center; font-size:40px; margin-top:-50px;
        font-family: 'Archivo', sans-serif; margin-bottom:20px;">Ultralytics YOLO Streamlit Application</h1></div>"""
        sub_title_cfg = """<div><h4 style="color:#042AFF; text-align:center; font-family: 'Archivo', sans-serif; 
        margin-top:-15px; margin-bottom:50px;">Experience real-time object detection on your webcam with the power 
        of Ultralytics YOLO! 🚀</h4></div>"""

        self.st.set_page_config(page_title="Ultralytics Streamlit App", layout="wide")
        self.st.markdown(menu_style_cfg, unsafe_allow_html=True)
        self.st.markdown(main_title_cfg, unsafe_allow_html=True)
        self.st.markdown(sub_title_cfg, unsafe_allow_html=True)

    def sidebar(self):
        with self.st.sidebar:
            logo = "https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg"
            self.st.image(logo, width=250)

        self.st.sidebar.title("User Configuration")
        self.enable_trk = self.st.sidebar.radio("Enable Tracking", ("Yes", "No"))
        self.conf = float(self.st.sidebar.slider("Confidence Threshold", 0.0, 1.0, self.conf, 0.01))
        self.iou = float(self.st.sidebar.slider("IoU Threshold", 0.0, 1.0, self.iou, 0.01))

    def configure(self):
        available_models = [x.replace("yolo", "YOLO") for x in GITHUB_ASSETS_STEMS if x.startswith("yolo11")]
        if self.model_path:
            available_models.insert(0, self.model_path.split(".pt")[0])

        selected_model = self.st.sidebar.selectbox("Model", available_models)

        with self.st.spinner("Model is downloading..."):
            self.model = YOLO(f"{selected_model.lower()}.pt")
            class_names = list(self.model.names.values())
        self.st.success("Model loaded successfully!")

        selected_classes = self.st.sidebar.multiselect("Classes", class_names, default=class_names[:3])
        self.selected_ind = [class_names.index(option) for option in selected_classes]

    class YOLOTransformer(VideoTransformerBase):
        def __init__(self, model, enable_trk, conf, iou, selected_ind):
            self.model = model
            self.enable_trk = enable_trk
            self.conf = conf
            self.iou = iou
            self.selected_ind = selected_ind

        def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
            import cv2
            import numpy as np

            img = frame.to_ndarray(format="bgr24")
            if self.enable_trk == "Yes":
                results = self.model.track(img, conf=self.conf, iou=self.iou,
                                           classes=self.selected_ind, persist=True)
            else:
                results = self.model(img, conf=self.conf, iou=self.iou, classes=self.selected_ind)
            annotated_img = results[0].plot()
            return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

       def webcam_detection(self):
         self.st.info("Bật camera để bắt đầu nhận diện gương mặt.")
         webrtc_streamer(
             key="face-detect",
             video_transformer_factory=lambda: self.YOLOTransformer(
                 self.model, self.enable_trk, self.conf, self.iou, self.selected_ind
             ),
             media_stream_constraints={"video": True, "audio": False},
             async_processing=True,
             video_frame_size=640,  # Điều chỉnh kích thước frame
             use_thread=True  # Sử dụng threading nếu cần thiết
         )


    def inference(self):
        self.web_ui()
        self.sidebar()
        self.configure()
        self.webcam_detection()


if __name__ == "__main__":
    import sys
    model = sys.argv[1] if len(sys.argv) > 1 else None
    Inference(model=model).inference()
