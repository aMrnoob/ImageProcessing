import streamlit as st
import numpy as np
from PIL import Image
import cv2

CONFIG = {
    "INPUT_WIDTH": 640,
    "INPUT_HEIGHT": 640,
    "SCORE_THRESHOLD": 0.5,
    "NMS_THRESHOLD": 0.4,
    "CONFIDENCE_THRESHOLD": 0.5,
    "FONT_FACE": cv2.FONT_HERSHEY_SIMPLEX,
    "FONT_SCALE": 0.5,
    "THICKNESS": 1,
    "COLORS": {
        "YELLOW": (0, 255, 255),
        "GREEN": (0, 255, 0),
        "BLACK": (0, 0, 0),
        "RED": (0, 0, 255),
        "WHITE": (255, 255, 255)
    },
    "MODEL_PATH": "Nhan_Dang_Trai_Cay/model/fruit.onnx"
}

def initialize_session_state():
    try:
        if st.session_state["LoadModel"] == True:
            print('✅ Đã load model rồi')
    except:
        st.session_state["LoadModel"] = True
        st.session_state["Net"] = cv2.dnn.readNet(CONFIG["MODEL_PATH"])
        print('🔁 Load model lần đầu')
    st.session_state["Net"].setPreferableBackend(0)
    st.session_state["Net"].setPreferableTarget(0)

def load_classes():
    filename_classes = 'Nhan_Dang_Trai_Cay/fruit_detection.txt'
    classes = None
    if filename_classes:
        with open(filename_classes, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
    return classes

def post_process(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    classes = load_classes()
    
    def drawPred(classId, conf, left, top, right, bottom):
        cv2.rectangle(frame, (left, top), (right, bottom), CONFIG["COLORS"]["GREEN"])
        label = '%.2f' % conf
        if classes:
            assert(classId < len(classes))
            label = '%s: %s' % (classes[classId], label)
        labelSize, baseLine = cv2.getTextSize(label, CONFIG["FONT_FACE"], CONFIG["FONT_SCALE"], CONFIG["THICKNESS"])
        top = max(top, labelSize[1])
        cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), 
                     CONFIG["COLORS"]["WHITE"], cv2.FILLED)
        cv2.putText(frame, label, (left, top), CONFIG["FONT_FACE"], CONFIG["FONT_SCALE"], 
                   CONFIG["COLORS"]["BLACK"], CONFIG["THICKNESS"])

    layerNames = st.session_state["Net"].getLayerNames()
    lastLayerId = st.session_state["Net"].getLayerId(layerNames[-1])
    lastLayer = st.session_state["Net"].getLayer(lastLayerId)
    postprocessing = 'yolov8'
    background_label_id = -1

    classIds = []
    confidences = []
    boxes = []
    
    if lastLayer.type == 'Region' or postprocessing == 'yolov8':
        if postprocessing == 'yolov8':
            box_scale_w = frameWidth / CONFIG["INPUT_WIDTH"]
            box_scale_h = frameHeight / CONFIG["INPUT_HEIGHT"]
        else:
            box_scale_w = frameWidth
            box_scale_h = frameHeight

        for out in outs:
            if postprocessing == 'yolov8':
                out = out[0].transpose(1, 0)
            for detection in out:
                scores = detection[4:]
                if background_label_id >= 0:
                    scores = np.delete(scores, background_label_id)
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > CONFIG["CONFIDENCE_THRESHOLD"]:
                    center_x = int(detection[0] * box_scale_w)
                    center_y = int(detection[1] * box_scale_h)
                    width = int(detection[2] * box_scale_w)
                    height = int(detection[3] * box_scale_h)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
    else:
        print('Unknown output layer type: ' + lastLayer.type)
        return

    outNames = st.session_state["Net"].getUnconnectedOutLayersNames()
    if len(outNames) > 1 or (lastLayer.type == 'Region' or postprocessing == 'yolov8') and 0 != cv2.dnn.DNN_BACKEND_OPENCV:
        indices = []
        classIds = np.array(classIds)
        boxes = np.array(boxes)
        confidences = np.array(confidences)
        unique_classes = set(classIds)
        for cl in unique_classes:
            class_indices = np.where(classIds == cl)[0]
            conf = confidences[class_indices]
            box = boxes[class_indices].tolist()
            nms_indices = cv2.dnn.NMSBoxes(box, conf, CONFIG["CONFIDENCE_THRESHOLD"], CONFIG["NMS_THRESHOLD"])
            indices.extend(class_indices[nms_indices])
    else:
        indices = np.arange(0, len(classIds))

    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
    
    return frame

def pre_process(input_image):
    scale = 0.00392
    mean = [0, 0, 0]
    
    frameHeight = input_image.shape[0]
    frameWidth = input_image.shape[1]
    inpWidth = CONFIG["INPUT_WIDTH"] 
    inpHeight = CONFIG["INPUT_HEIGHT"]
    blob = cv2.dnn.blobFromImage(input_image, size=(inpWidth, inpHeight), swapRB=True, ddepth=cv2.CV_8U)
    st.session_state["Net"].setInput(blob, scalefactor=scale, mean=mean)
    if st.session_state["Net"].getLayer(0).outputNameToIndex('im_info') != -1:
        input_image = cv2.resize(input_image, (inpWidth, inpHeight))
        st.session_state["Net"].setInput(np.array([[inpHeight, inpWidth, 1.6]], dtype=np.float32), 'im_info')
    outNames = st.session_state["Net"].getUnconnectedOutLayersNames()
    outs = st.session_state["Net"].forward(outNames)
    return input_image, outs

def process_image(uploaded_file):
    image = Image.open(uploaded_file)
    frame = np.array(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    col1, col2 = st.columns([1,1])
    with col1:
        st.image(image, use_column_width=True)
    if st.button('🚀 Nhận dạng'):
        with st.spinner('Đang xử lý...'):
            processed_frame, outs = pre_process(frame)
            result_img = post_process(frame, outs)
            color_converted = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_converted)
            with col2:
                st.image(pil_image, use_column_width=True)

def run():
    st.title('🍎 Nhận dạng trái cây')
    st.markdown("Ứng dụng nhận dạng các loại trái cây bằng mô hình YOLOv8")
    initialize_session_state()
    img_file_buffer = st.file_uploader("📁 Tải ảnh lên", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        process_image(img_file_buffer)
