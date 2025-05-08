import streamlit as st
import numpy as np
from PIL import Image
import cv2

def run():
    st.title("🚦 Nhận dạng biển báo đường bộ")
    
    # Initialize model and classes if not already loaded
    if 'is_loaded_sign' not in st.session_state:
        st.session_state["Net"] = cv2.dnn.readNet("Nhan_Dang_Bien_Bao/road_sign.onnx")
        with open('Nhan_Dang_Bien_Bao/road_signs_classes.txt', 'rt') as f:
            st.session_state["Classes"] = f.read().rstrip('\n').split('\n')
        
        # Set backend preferences
        st.session_state["Net"].setPreferableBackend(0)
        st.session_state["Net"].setPreferableTarget(0)
        st.session_state["is_loaded_sign"] = True
    
    # Detection parameters
    confThreshold = 0.5
    nmsThreshold = 0.4
    scale = 0.00392  # Same as original
    mean = [0, 0, 0]
    mywidth = 640
    myheight = 640
    
    # File uploader
    uploaded_file = st.file_uploader("📁 Tải lên ảnh biển báo", type=["jpg", "png", "jpeg", "bmp"])
    
    # Create two columns for input and output
    col1, col2 = st.columns([1.2, 1])
    
    if uploaded_file is not None:
        # Load and process image
        image = Image.open(uploaded_file).convert("RGB")
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        with col1:
            st.image(image, caption="Ảnh đầu vào", use_column_width=True)
        
        if st.button("Nhận dạng"):
            # Get dimensions
            frameHeight = frame.shape[0]
            frameWidth = frame.shape[1]
            
            # Create blob from image - match exactly with original
            inpWidth = mywidth
            inpHeight = myheight
            blob = cv2.dnn.blobFromImage(frame, size=(inpWidth, inpHeight), swapRB=True, ddepth=cv2.CV_8U)
            
            # Get output names
            outNames = st.session_state["Net"].getUnconnectedOutLayersNames()
            
            # Set input and parameters exactly like original
            st.session_state["Net"].setInput(blob, scalefactor=scale, mean=mean)
            
            # Handle special case for certain models
            try:
                if st.session_state["Net"].getLayer(0).outputNameToIndex('im_info') != -1:
                    frame = cv2.resize(frame, (inpWidth, inpHeight))
                    st.session_state["Net"].setInput(np.array([[inpHeight, inpWidth, 1.6]], dtype=np.float32), 'im_info')
            except:
                pass  # If this fails, just continue
            
            # Forward pass
            outs = st.session_state["Net"].forward(outNames)
            
            # Process outputs using a similar approach to original code
            def postprocess(frame, outs):
                frameHeight = frame.shape[0]
                frameWidth = frame.shape[1]
                
                # Get model layer info
                layerNames = st.session_state["Net"].getLayerNames()
                lastLayerId = st.session_state["Net"].getLayerId(layerNames[-1])
                lastLayer = st.session_state["Net"].getLayer(lastLayerId)
                
                classIds = []
                confidences = []
                boxes = []
                
                # YOLOv8 format processing - from original
                box_scale_w = frameWidth / mywidth
                box_scale_h = frameHeight / myheight
                
                for out in outs:
                    # Handle YOLOv8 format
                    out = out[0].transpose(1, 0)
                    
                    for detection in out:
                        scores = detection[4:]
                        classId = np.argmax(scores)
                        confidence = scores[classId]
                        
                        if confidence > confThreshold:
                            # Scale boxes to original image size
                            center_x = int(detection[0] * box_scale_w)
                            center_y = int(detection[1] * box_scale_h)
                            width = int(detection[2] * box_scale_w)
                            height = int(detection[3] * box_scale_h)
                            
                            # Calculate box coordinates
                            left = int(center_x - width / 2)
                            top = int(center_y - height / 2)
                            
                            # Add to lists
                            classIds.append(classId)
                            confidences.append(float(confidence))
                            boxes.append([left, top, width, height])
                
                # Apply non-maximum suppression with the same approach as original
                indices = []
                if len(boxes) > 0:
                    # Convert to numpy arrays
                    classIds = np.array(classIds)
                    boxes = np.array(boxes)
                    confidences = np.array(confidences)
                    
                    # Process by class - exactly as in original
                    unique_classes = set(classIds)
                    for cl in unique_classes:
                        class_indices = np.where(classIds == cl)[0]
                        conf = confidences[class_indices]
                        box = boxes[class_indices].tolist()
                        nms_indices = cv2.dnn.NMSBoxes(box, conf, confThreshold, nmsThreshold)
                        
                        # Handle empty results and OpenCV version differences
                        if len(nms_indices) > 0:
                            if isinstance(nms_indices, np.ndarray) and nms_indices.ndim > 1:
                                nms_indices = nms_indices.flatten()
                            
                            # Add indices to result
                            indices.extend(class_indices[nms_indices])
                
                # Draw results
                for i in indices:
                    box = boxes[i]
                    left = box[0]
                    top = box[1]
                    width = box[2]
                    height = box[3]
                    
                    # Draw box
                    cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
                    
                    # Add label
                    label = '%.2f' % confidences[i]
                    if st.session_state["Classes"]:
                        label = '%s: %s' % (st.session_state["Classes"][classIds[i]], label)
                    
                    # Draw label
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    top = max(top, labelSize[1])
                    cv2.rectangle(frame, (left, top - labelSize[1]), 
                                (left + labelSize[0], top + baseLine), 
                                (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (left, top), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                
                return frame
            
            # Process the frame
            processed_frame = postprocess(frame, outs)
            
            # Convert back to RGB for display
            result_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            with col2:
                st.image(result_image, caption="Kết quả nhận dạng", use_column_width=True)