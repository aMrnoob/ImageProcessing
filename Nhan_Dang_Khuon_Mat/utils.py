import os
import numpy as np
import cv2
import onnxruntime as ort
from numpy.linalg import norm
from Nhan_Dang_Khuon_Mat.yunet import YuNet
import streamlit as st

detector = YuNet(
    modelPath="Nhan_Dang_Khuon_Mat/model/face_detection_yunet_2023mar.onnx",
    inputSize=[640, 640],
    confThreshold=0.8,
    nmsThreshold=0.3,
    topK=5000,
    backendId=cv2.dnn.DNN_BACKEND_DEFAULT,
    targetId=cv2.dnn.DNN_TARGET_CPU
)

recognizer = ort.InferenceSession("Nhan_Dang_Khuon_Mat/model/face_recognition_sface_2021dec.onnx")

def detect_faces(img, conf_thresh=0.9):
    """Detect faces in an image and return their bounding boxes"""
    if img is None or img.size == 0:
        return []
        
    h, w = img.shape[:2]
    detector.setInputSize([w, h])
    results = detector.infer(img)
    boxes = []

    if results is not None:
        for x, y, w_box, h_box, *_, conf in results:
            if conf >= conf_thresh:
                boxes.append([int(x), int(y), int(x + w_box), int(y + h_box)])
    
    return boxes

def preprocess_face(img, box, margin=0.0):
    """Extract and preprocess face for recognition"""
    if img is None or img.size == 0:
        return None
        
    x1, y1, x2, y2 = box
    h, w = img.shape[:2]
    
    margin_x = int((x2 - x1) * margin)
    margin_y = int((y2 - y1) * margin)
    
    x1 = max(0, x1 - margin_x)
    y1 = max(0, y1 - margin_y)
    x2 = min(w, x2 + margin_x)
    y2 = min(h, y2 + margin_y)
    
    face = img[y1:y2, x1:x2]
    if face.size == 0:
        return None
        
    face = cv2.resize(face, (112, 112))
    
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    
    face_tensor = np.transpose(face, (2, 0, 1))[np.newaxis, :]
    return face_tensor

def get_embedding(face_tensor):
    """Get face embedding from preprocessed face tensor"""
    if face_tensor is None:
        return None
        
    input_name = recognizer.get_inputs()[0].name
    emb = recognizer.run(None, {input_name: face_tensor})[0][0]
    
    norm_emb = emb / np.linalg.norm(emb)
    return norm_emb

def load_known_faces(folder="Nhan_Dang_Khuon_Mat/faces_recognized"):
    """Load known faces from directory with person subfolders"""
    known = {}
    
    if not os.path.exists(folder):
        print(f"❌ Directory not found: {folder}")
        return known
    
    # Get all subdirectories (each representing a person)
    person_dirs = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
    
    if not person_dirs:
        print(f"⚠️ No person directories found in {folder}")
        # Fall back to original behavior - look for images directly in the folder
        for file in os.listdir(folder):
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            name = os.path.splitext(file)[0]
            img_path = os.path.join(folder, file)
            process_face_image(img_path, name, known)
    else:
        # Process each person's directory
        for person_name in person_dirs:
            person_dir = os.path.join(folder, person_name)
            print(f"Processing directory for {person_name}...")
            
            # Get all image files in the person's directory
            image_files = [f for f in os.listdir(person_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not image_files:
                print(f"⚠️ No images found for {person_name}")
                continue
                
            # Process each image for this person
            for i, file in enumerate(image_files):
                img_path = os.path.join(person_dir, file)
                # Use person_name as the base name and add index if multiple images
                face_name = f"{person_name}_{i}" if len(image_files) > 1 else person_name
                process_face_image(img_path, face_name, known)
    
    print(f"✅ Loaded {len(known)} known faces")
    return known

def compute_similarity(emb1, emb2):
    """Compute similarity between two face embeddings"""
    similarity = np.dot(emb1, emb2)
    distance = 1.0 - similarity
    return distance

def recognize_faces(img, known_faces, threshold=0.2):
    """Detect and recognize faces in an image"""
    if img is None or img.size == 0 or not known_faces:
        return img.copy() if img is not None and img.size > 0 else None
        
    boxes = detect_faces(img)
    annotated = img.copy()

    for box in boxes:
        face_tensor = preprocess_face(img, box, margin=0.1)
        if face_tensor is None:
            continue
            
        emb = get_embedding(face_tensor)
        if emb is None:
            continue
            
        best_match = "Unknown"
        best_dist = float("inf")
        
        for name, known_emb in known_faces.items():
            dist = compute_similarity(emb, known_emb)
            if dist < best_dist:
                base_name = name.rsplit('_', 1)[0]
                best_match = base_name
                best_dist = dist

        label = f"{best_match} ({best_dist:.2f})" if best_dist < threshold else f"Unknown ({best_dist:.2f})"
        color = (0, 255, 0) if best_dist < threshold else (0, 0, 255)

        x1, y1, x2, y2 = box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
    return annotated

def process_face_image(img_path, name, known_dict):
    """Process a single face image and add its embedding to the known_dict"""
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"❌ Could not read image: {img_path}")
        return

    boxes = detect_faces(img)
    if not boxes:
        print(f"❌ No faces detected in {img_path}")
        return
        
    if len(boxes) > 1:
        print(f"⚠️ Found {len(boxes)} faces in {img_path}, using the first one")
    
    face_tensor = preprocess_face(img, boxes[0], margin=0.1)
    if face_tensor is None:
        print(f"❌ Failed to preprocess face in {img_path}")
        return
        
    emb = get_embedding(face_tensor)
    if emb is not None:
        known_dict[name] = emb
        print(f"  ✓ Added face embedding for {name}")
    else:
        print(f"❌ Failed to get embedding for {img_path}")

def recognize_faces_video(video_path, known_faces, threshold=0.2):
    """Process video and recognize faces in each frame"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("❌ Cannot open video.")
        return

    stframe = st.empty()
    
    if not known_faces:
        known_faces = load_known_faces()
        if not known_faces:
            st.warning("⚠️ No known faces loaded. Everyone will be marked as 'Unknown'.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        annotated = recognize_faces(frame, known_faces, threshold)
        if annotated is not None:
            stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    
    cap.release()