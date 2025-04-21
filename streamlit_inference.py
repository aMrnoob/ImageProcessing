import io
from typing import Any

import cv2
import av  # PyAV dùng bởi webrtc-streamer
import asyncio
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from ultralytics import YOLO
from ultralytics.utils import LOGGER
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.downloads import GITHUB_ASSETS_STEMS


class Inference:
    def __init__(self, **kwargs: Any):
        check_requirements("streamlit>=1.29.0")
        import streamlit as st

        self.st = st
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
        self.model_path = None
        if self.temp_dict["model"] is not None:
            self.model_path = self.temp_dict["model"]

        LOGGER.info(f"Ultralytics Solutions: ✅ {self.temp_dict}")

    def web_ui(self):
        self.st.set_page_config(page_title="Ultralytics Streamlit App", layout="wide")
        menu_style_cfg = """<style>MainMenu {visibility: hidden;}</style>"""
        main_title_cfg = """<div><h1 style="color:#FF64DA; text-align:center; font-size:40px; margin-top:-50px;
        font-family: 'Archivo', sans-serif; margin-bottom:20px;">Ultralytics YOLO Streamlit Application</h1></div>"""
        sub_title_cfg = """<div><h4 style="color:#042AFF; text-align:center; font-family: 'Archivo', sans-serif; 
        margin-top:-15px; margin-bottom:50px;">Experience real-time object detection on your webcam with the power 
        of Ultralytics YOLO! 🚀</h4></div>"""

        self.st.markdown(menu_style_cfg, unsafe_allow_html=True)
        self.st.markdown(main_title_cfg, unsafe_allow_html=True)
        self.st.markdown(sub_title_cfg, unsafe_allow_html=True)

    def sidebar(self):
        with self.st.sidebar:
            logo = "https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg"
            self.st.image(logo, width=250)

        self.st.sidebar.title("User Configuration")
        self.source = self.st.sidebar.selectbox("Video", ("webcam", "video"))
        self.enable_trk = self.st.sidebar.radio("Enable Tracking", ("Yes", "No"))
        self.conf = float(self.st.sidebar.slider("Confidence Threshold", 0.0, 1.0, self.conf, 0.01))
        self.iou = float(self.st.sidebar.slider("IoU Threshold", 0.0, 1.0, self.iou, 0.01))

        col1, col2 = self.st.columns(2)
        self.org_frame = col1.empty()
        self.ann_frame = col2.empty()

    def source_upload(self):
        self.vid_file_name = ""
        if self.source == "video":
            vid_file = self.st.sidebar.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv"])
            if vid_file is not None:
                g = io.BytesIO(vid_file.read())
                with open("ultralytics.mp4", "wb") as out:
                    out.write(g.read())
                self.vid_file_name = "ultralytics.mp4"
        elif self.source == "webcam":
            self.vid_file_name = 0

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

        if not isinstance(self.selected_ind, list):
            self.selected_ind = list(self.selected_ind)

    class YOLOVideoProcessor(VideoProcessorBase):
        def __init__(self):
            self.model = None
            self.enable_trk = "No"
            self.conf = 0.25
            self.iou = 0.45
            self.selected_ind = []

        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            if self.enable_trk == "Yes":
                results = self.model.track(img, conf=self.conf, iou=self.iou, classes=self.selected_ind, persist=True)
            else:
                results = self.model(img, conf=self.conf, iou=self.iou, classes=self.selected_ind)
            annotated_img = results[0].plot()
            return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

    def inference(self):
        self.web_ui()
        self.sidebar()
        self.source_upload()
        self.configure()

        if self.source == "webcam":
            webrtc_ctx = webrtc_streamer(
                key="yolo",
                video_processor_factory=self.YOLOVideoProcessor,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
            )
            if webrtc_ctx.video_processor:
                webrtc_ctx.video_processor.model = self.model
                webrtc_ctx.video_processor.enable_trk = self.enable_trk
                webrtc_ctx.video_processor.conf = self.conf
                webrtc_ctx.video_processor.iou = self.iou
                webrtc_ctx.video_processor.selected_ind = self.selected_ind

        elif self.source == "video":
            self.st.warning("Video file processing chưa được hỗ trợ với WebRTC.")


# ⚠️ Đảm bảo chạy event loop đúng cách trong Python 3.12+
if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    import sys

    args = len(sys.argv)
    model = sys.argv[1] if args > 1 else None
    Inference(model=model).inference()
