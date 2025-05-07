import cv2
import numpy as np
from ultralytics import YOLO
import os
from pathlib import Path

class LicensePlateDetector:
    def __init__(self, model_path=None):
        self.model_dir = Path(r"C:\Users\Admin\Documents\Github\ImageProcessing\ImageProcessing\Nhan_Dang_Bien_So_Xe")
        if not self.model_dir.exists():
            self.model_dir.mkdir(exist_ok=True)
            
        self.model_path = model_path
        if self.model_path is None:
            self.model_path = self.model_dir / "license_plate_detector.pt"
            
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Mô hình không được tìm thấy tại {self.model_path}")
        
        try:
            self.model = YOLO(str(self.model_path))
            print(f"Đã tải mô hình YOLOv8 từ {self.model_path}")
        except Exception as e:
            print(f"Lỗi khi tải mô hình YOLOv8: {e}")
            self.model = None
        
        self.conf_threshold = 0.5

    def detect_plates(self, image):
        if image is None:
            print("Không thể đọc ảnh.")
            return None
        
        marked_image = image.copy()
        
        results = self.model(image, conf=self.conf_threshold)
        
        plates_found = False
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()
                
                x, y = int(x1), int(y1)
                w, h = int(x2 - x1), int(y2 - y1)
                
                cv2.rectangle(marked_image, (x, y), (x+w, y+h), (0, 0, 255), 3)
                
                text = f"Bien so: {conf:.2f}"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                text_x = x
                text_y = y - 10
                cv2.rectangle(marked_image, (text_x, text_y - text_size[1]), 
                              (text_x + text_size[0], text_y + 5), (0, 0, 255), -1)
                
                cv2.putText(marked_image, text, (text_x, text_y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                
                plates_found = True
                
        if not plates_found:
            print("Không tìm thấy biển số xe trong ảnh.")
            
        return marked_image
