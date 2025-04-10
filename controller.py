import streamlit as st

st.set_page_config(page_title="Xử lý ảnh số", layout="wide")

st.sidebar.title("📚 Danh mục chức năng")
menu = st.sidebar.selectbox(
    "Chọn một chức năng để bắt đầu:",
    [
        "🧮 Giải phương trình bậc 2",
        "🎭 Nhận diện khuôn mặt",
        "👁️ Nhận dạng đối tượng (YOLOv8)",
        "🍎 Nhận dạng trái cây",
        "🔢 Nhận dạng chữ số"
    ]
)

st.title("🧠 Ứng dụng Xử lý Ảnh Số")

if menu == "🧮 Giải phương trình bậc 2":
    from Giai_PT_Bac_2.app import run as Giai_PT_Bac_2_app
    Giai_PT_Bac_2_app()

elif menu == "🎭 Nhận diện khuôn mặt":
    from Nhan_Dang_Khuon_Mat.app import run as Nhan_Dang_Khuon_Mat_app
    Nhan_Dang_Khuon_Mat_app()

elif menu == "👁️ Nhận dạng đối tượng (YOLOv8)":
    from Nhan_Dang_Doi_Tuong.app import run as Nhan_Dang_Doi_Tuong__app
    Nhan_Dang_Doi_Tuong__app()

elif menu == "🍎 Nhận dạng trái cây":
    from Nhan_Dang_Trai_Cay.app import run as Nhan_Dang_Trai_Cay_app
    Nhan_Dang_Trai_Cay_app()

elif menu == "🔢 Nhận dạng chữ số":
    from Nhan_Dang_Chu_So.app import run as Nhan_Dang_Chu_So_app
    Nhan_Dang_Chu_So_app


