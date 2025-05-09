import cv2
import streamlit as st
import pandas as pd

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(r"Nhan_Dang_Mau_Sac\colors.csv", names=index, header=None)

def run():
    st.title("🎨 Nhận Dạng Màu Sắc Qua Camera")

    st.write("Bật camera và đặt vật thể vào giữa màn hình để nhận dạng màu sắc.")
    
    loadColor()

def loadColor():
    camera_on = st.checkbox("📷 Bật/Tắt Camera")
    if camera_on:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Không thể kết nối với camera. Vui lòng kiểm tra lại.")
            return
        
        cap.set(3, 720)
        cap.set(4, 1280)
        
        video_placeholder = st.image([])

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Không đọc được hình ảnh từ camera.")
                break

            frame = cv2.flip(frame, 1)
            
            # Lấy điểm trung tâm
            x, y = int(frame.shape[1]/2), int(frame.shape[0]/2)
            b, g, r = frame[y, x]
            b, g, r = int(b), int(g), int(r)
            
            color_name = getColorName(b, g, r)
            drawSquare(frame, x, y)
            putText(frame, x, y, color_name, b, g, r)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame, channels="RGB")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

def drawSquare(img, x, y):
    YELLOW = (255, 255, 255)
    BLUE = (255, 225, 255)
    
    cv2.line(img, (x - 150, y - 150), (x - 100, y - 150), YELLOW, 5)
    cv2.line(img, (x - 150, y - 150), (x - 150, y - 100), BLUE, 5)
    
    cv2.line(img, (x + 150, y - 150), (x + 100, y - 150), YELLOW, 5)
    cv2.line(img, (x + 150, y - 150), (x + 150, y - 100), BLUE, 5)
    
    cv2.line(img, (x + 150, y + 150), (x + 100, y + 150), YELLOW, 5)
    cv2.line(img, (x + 150, y + 150), (x + 150, y + 100), BLUE, 5)
    
    cv2.line(img, (x - 150, y + 150), (x - 100, y + 150), YELLOW, 5)
    cv2.line(img, (x - 150, y + 150), (x - 150, y + 100), BLUE, 5)
    
    cv2.circle(img, (x, y), 3, (255, 255, 255), -1)

def getColorName(b, g, r):
    minimum = 1000 
    cname = "Không xác định"
    for i in range(len(csv)):
        d = abs(b - int(csv.loc[i, "B"])) + abs(g - int(csv.loc[i, "G"])) + abs(r - int(csv.loc[i, "R"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def putText(img, x, y, color_name, b, g, r):
    cv2.rectangle(img, (0, 0), (x+350, y-180), (b, g, r), -1)
    text = f"{color_name} | R={r} G={g} B={b}"
    cv2.putText(img, text, (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
