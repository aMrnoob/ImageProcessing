import streamlit as st

st.set_page_config(page_title="Xử lý ảnh số", layout="wide")

st.sidebar.title("📚 Danh mục chức năng")
menu = st.sidebar.selectbox(
    "Chọn một chức năng để bắt đầu:",
    [
        "🎭 Nhận diện khuôn mặt",
        "🍎 Nhận dạng đối tượng (YOLOv8)",
        "🧪 Xử lý ảnh số"
    ]
)

st.title("🧠 Ứng dụng Xử lý Ảnh Số")

if menu == "🎭 Nhận diện khuôn mặt":
    from face_recognition_app.app import run as run_face_app
    run_face_app()

elif menu == "🍎 Nhận dạng đối tượng (YOLOv8)":
    st.info("👉 Bạn đã chọn: Nhận dạng đối tượng (YOLOv8)")

elif menu == "🧪 Xử lý ảnh số":
    st.info("👉 Bạn đã chọn: Xử lý ảnh số")
