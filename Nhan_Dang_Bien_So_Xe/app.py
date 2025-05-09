import streamlit as st
import cv2
import numpy as np
from Nhan_Dang_Bien_So_Xe.LicensePlateDetector import LicensePlateDetector

def run():
    """Ứng dụng nhận dạng biển số xe đơn giản"""
    st.title("🚗 Nhận Dạng Biển Số Xe")
    
    with st.spinner("Đang tải..."):
        detector = LicensePlateDetector()
    
    st.header("Tải lên ảnh của bạn")
    uploaded_file = st.file_uploader("Chọn ảnh có biển số xe", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        st.image(image, channels="BGR", use_container_width=True, caption="Ảnh gốc")
        
        if st.button("Phát hiện biển số", key="detect_uploaded"):
            with st.spinner("Đang xử lý ảnh..."):
                result_image = detector.detect_plates(image)
                
                st.image(result_image, channels="BGR", use_container_width=True, caption="Kết quả phát hiện")
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center">
            <p>Ứng dụng phát hiện biển số xe</p>
        </div>
        """,
        unsafe_allow_html=True
    )
