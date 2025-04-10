import streamlit as st

st.set_page_config(page_title="Xử lý ảnh số", layout="wide")

st.sidebar.title("📚 Danh mục chức năng")
menu = st.sidebar.selectbox(
    "Chọn một chức năng để bắt đầu:",
    [
        "🎭 Nhận diện khuôn mặt",
        "👁️ Nhận dạng đối tượng (YOLOv8)",
        "🍎 Nhận dạng trái cây",
        "🔢 Nhận dạng chữ số"
    ]
)

st.title("🧠 Ứng dụng Xử lý Ảnh Số")

if menu == "🎭 Nhận diện khuôn mặt":
    from Nhan_Dang_Khuon_Mat.app import run as run_face_app
    run_face_app()

elif menu == "👁️ Nhận dạng đối tượng (YOLOv8)":
    from Nhan_Dang_Doi_Tuong.app import run as run_face_app
    run_face_app()

elif menu == "🍎 Nhận dạng trái cây":
    from Nhan_Dang_Trai_Cay.app import run as run_face_app
    run_face_app()

elif menu == "🔢 Nhận dạng chữ số":
    from Nhan_Dang_Chu_So.app import run as run_face_app
    run_face_app()


