from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

class YOLOProcessor(VideoProcessorBase):
    def __init__(self):
        self.model = None
        self.enable_trk = False
        self.conf = 0.25
        self.iou = 0.45
        self.selected_ind = []

    def set_model(self, model, enable_trk, conf, iou, selected_ind):
        self.model = model
        self.enable_trk = enable_trk
        self.conf = conf
        self.iou = iou
        self.selected_ind = selected_ind

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if self.enable_trk == "Yes":
            results = self.model.track(img, conf=self.conf, iou=self.iou,
                                       classes=self.selected_ind, persist=True)
        else:
            results = self.model(img, conf=self.conf, iou=self.iou, classes=self.selected_ind)
        annotated_img = results[0].plot()
        return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")
