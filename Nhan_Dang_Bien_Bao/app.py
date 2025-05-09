import streamlit as st
import numpy as np
from PIL import Image
import cv2

def run():
    st.title("🚦 Nhận dạng biển báo đường bộ")
    
    if 'is_loaded_sign' not in st.session_state:
        st.session_state["Net"] = cv2.dnn.readNet("Nhan_Dang_Bien_Bao/road_sign.onnx")
        with open('Nhan_Dang_Bien_Bao/road_signs_classes.txt', 'rt') as f:
            st.session_state["Classes"] = f.read().rstrip('\n').split('\n')
        
        st.session_state["Net"].setPreferableBackend(0)
        st.session_state["Net"].setPreferableTarget(0)
        st.session_state["is_loaded_sign"] = True
    
    confThreshold = 0.5
    nmsThreshold = 0.4
    scale = 0.00392  
    mean = [0, 0, 0]
    mywidth = 640
    myheight = 640
    
    uploaded_file = st.file_uploader("📁 Tải lên ảnh biển báo", type=["jpg", "png", "jpeg", "bmp"])
    
    col1, col2 = st.columns([1.2, 1])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        with col1:
            st.image(image, caption="Ảnh đầu vào", use_column_width=True)
        
        if st.button("Nhận dạng"):
            frameHeight = frame.shape[0]
            frameWidth = frame.shape[1]
            
            inpWidth = mywidth
            inpHeight = myheight
            blob = cv2.dnn.blobFromImage(frame, size=(inpWidth, inpHeight), swapRB=True, ddepth=cv2.CV_8U)
            
            outNames = st.session_state["Net"].getUnconnectedOutLayersNames()
            
            st.session_state["Net"].setInput(blob, scalefactor=scale, mean=mean)
            
            try:
                if st.session_state["Net"].getLayer(0).outputNameToIndex('im_info') != -1:
                    frame = cv2.resize(frame, (inpWidth, inpHeight))
                    st.session_state["Net"].setInput(np.array([[inpHeight, inpWidth, 1.6]], dtype=np.float32), 'im_info')
            except:
                pass  
            
            outs = st.session_state["Net"].forward(outNames)
            
            def postprocess(frame, outs):
                frameHeight = frame.shape[0]
                frameWidth = frame.shape[1]
                
                layerNames = st.session_state["Net"].getLayerNames()
                lastLayerId = st.session_state["Net"].getLayerId(layerNames[-1])
                lastLayer = st.session_state["Net"].getLayer(lastLayerId)
                
                classIds = []
                confidences = []
                boxes = []
                
                box_scale_w = frameWidth / mywidth
                box_scale_h = frameHeight / myheight
                
                for out in outs:
                    out = out[0].transpose(1, 0)
                    
                    for detection in out:
                        scores = detection[4:]
                        classId = np.argmax(scores)
                        confidence = scores[classId]
                        
                        if confidence > confThreshold:
                            center_x = int(detection[0] * box_scale_w)
                            center_y = int(detection[1] * box_scale_h)
                            width = int(detection[2] * box_scale_w)
                            height = int(detection[3] * box_scale_h)
                            
                            left = int(center_x - width / 2)
                            top = int(center_y - height / 2)
                            
                            classIds.append(classId)
                            confidences.append(float(confidence))
                            boxes.append([left, top, width, height])
                
                indices = []
                if len(boxes) > 0:
                    classIds = np.array(classIds)
                    boxes = np.array(boxes)
                    confidences = np.array(confidences)
                    
                    unique_classes = set(classIds)
                    for cl in unique_classes:
                        class_indices = np.where(classIds == cl)[0]
                        conf = confidences[class_indices]
                        box = boxes[class_indices].tolist()
                        nms_indices = cv2.dnn.NMSBoxes(box, conf, confThreshold, nmsThreshold)
                        
                        if len(nms_indices) > 0:
                            if isinstance(nms_indices, np.ndarray) and nms_indices.ndim > 1:
                                nms_indices = nms_indices.flatten()
                            
                            indices.extend(class_indices[nms_indices])
                
                for i in indices:
                    box = boxes[i]
                    left = box[0]
                    top = box[1]
                    width = box[2]
                    height = box[3]
                    
                    cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
                    
                    label = '%.2f' % confidences[i]
                    if st.session_state["Classes"]:
                        label = '%s: %s' % (st.session_state["Classes"][classIds[i]], label)
                    
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    top = max(top, labelSize[1])
                    cv2.rectangle(frame, (left, top - labelSize[1]), 
                                (left + labelSize[0], top + baseLine), 
                                (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (left, top), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                
                return frame
            
            processed_frame = postprocess(frame, outs)
            
            result_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            with col2:
                st.image(result_image, caption="Kết quả nhận dạng", use_container_width=True)