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
        "🔢 Nhận dạng chữ số",
        "📝 Bài tập chương"
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
    Nhan_Dang_Chu_So_app()

elif menu == "📝 Bài tập chương":
    st.sidebar.subheader("📖 Chọn chương")
    chapter = st.sidebar.selectbox(
        "Chọn chương bạn muốn thực hành:",
        [
            "Chương 3: Các phép toán điểm ảnh",
            "Chương 4: Các phép toán không gian",
            "Chương 9: Xử lý ảnh hình thái"
        ]
    )
    
    if chapter == "Chương 3: Các phép toán điểm ảnh":
        from Bai_Tap_Chuong.Chuong_03 import run as Chuong_3_app
        Chuong_3_app()
        
    elif chapter == "Chương 4: Các phép toán không gian":
        from Bai_Tap_Chuong.Chuong_04 import run as Chuong_4_app
        Chuong_4_app()
        
    elif chapter == "Chương 9: Xử lý ảnh hình thái":
        from Bai_Tap_Chuong.Chuong_09 import run as Chuong_9_app
        Chuong_9_app()