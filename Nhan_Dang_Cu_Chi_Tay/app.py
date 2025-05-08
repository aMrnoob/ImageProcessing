import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector

def run():
    st.title("🖐️ Nhận diện cử chỉ tay theo điểm đặc trưng")
    st.write("Dựa trên trạng thái các ngón tay (giơ lên/gập lại) để nhận dạng các cử chỉ.")

    detector = HandDetector(maxHands=1, detectionCon=0.8)
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while True:
        success, frame = cap.read()
        if not success:
            st.warning("Không thể truy cập webcam.")
            break

        frame = cv2.flip(frame, 1)
        hands, img = detector.findHands(frame)

        gesture_text = "Khong co tay"  

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)

            if fingers == [0, 1, 0, 0, 0]:
                gesture_text = "Ngon tro (1)"
            elif fingers == [0, 1, 1, 1, 0]:
                gesture_text = "3 ngon (3)"
            elif fingers == [0, 1, 1, 1, 1]:
                gesture_text = "4 ngon (4)"
            elif fingers == [1, 1, 1, 1, 1]:
                gesture_text = "Ban tay mo (5)"
            elif fingers == [0, 0, 0, 0, 0]:
                gesture_text = "Nam tay"
            elif fingers == [0, 1, 1, 0, 0]:
                gesture_text = "Xin chao"
            elif fingers == [0, 0, 0, 1, 1]:
                gesture_text = "OK / Like"
            else:
                gesture_text = f"Tu the tay: {fingers}"

            cv2.putText(img, gesture_text, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        stframe.image(img, channels="BGR", use_container_width=True)

    cap.release()
