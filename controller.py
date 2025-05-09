import streamlit as st
from PIL import Image

st.set_page_config(page_title="Xử lý ảnh số", layout="wide")

col1, col2 = st.columns([1, 5])
with col1:
    logo = Image.open("C:/Users/Admin/Documents/Github/ImageProcessing/ImageProcessing/logo_ute.png")
    st.image(logo, width=100)

with col2:
    st.markdown("""
        <div style='font-size: 20px; font-weight: bold; line-height: 1.6;'>
            👨‍🏫 <b>Giảng viên phụ trách:</b> Thầy Trần Tiến Đức  
            📚 <b>Bộ môn:</b> Xử lý ảnh số  
            🏫 <b>Trường:</b> Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh
        </div>
        <br>
        <div style='font-size: 18px; line-height: 1.6;'>
            👥 <b>Thành viên nhóm:</b><br>
            ▪️ Tô Hữu Đức – 22110311<br>
            ▪️ Đỗ Văn Thường – 22110432
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.sidebar.title("📚 Danh mục chức năng")
menu = st.sidebar.selectbox(
    "Chọn một chức năng để bắt đầu:",
    [
        "🧮 Giải phương trình bậc 2",
        "🎭 Nhận dạng khuôn mặt",
        "😊 Nhận dạng cảm xúc", 
        "👁️ Nhận dạng đối tượng",
        "🍎 Nhận dạng trái cây",
        "🔢 Nhận dạng chữ số",
        "🎨 Nhận dạng màu sắc", 
        "🚗 Nhận dạng biển số xe", 
        "🖐 Nhận dạng cử chỉ tay",
        "🚦 Nhận dạng biển báo đường bộ",
        "📝 Bài tập chương",
    ]
)

st.title("🧠 Ứng dụng Xử lý Ảnh Số")

if menu == "🧮 Giải phương trình bậc 2":
    from Giai_PT_Bac_2.app import run as Giai_PT_Bac_2_app
    Giai_PT_Bac_2_app()

elif menu == "🎭 Nhận dạng khuôn mặt":
    from Nhan_Dang_Khuon_Mat.app import run as Nhan_Dang_Khuon_Mat_app
    Nhan_Dang_Khuon_Mat_app()

elif menu == "😊 Nhận dạng cảm xúc":  
    from Nhan_Dang_Cam_Xuc.app import run as Nhan_Dang_Cam_Xuc_app
    Nhan_Dang_Cam_Xuc_app()

elif menu == "👁️ Nhận dạng đối tượng":
    from Nhan_Dang_Doi_Tuong.app import run as Nhan_Dang_Doi_Tuong_app
    Nhan_Dang_Doi_Tuong_app()

elif menu == "🍎 Nhận dạng trái cây":
    from Nhan_Dang_Trai_Cay.app import run as Nhan_Dang_Trai_Cay_app
    Nhan_Dang_Trai_Cay_app()

elif menu == "🔢 Nhận dạng chữ số":
    from Nhan_Dang_Chu_So.app import run as Nhan_Dang_Chu_So_app
    Nhan_Dang_Chu_So_app()

elif menu == "🎨 Nhận dạng màu sắc":
    from Nhan_Dang_Mau_Sac.app import run as Nhan_Dang_Mau_Sac_app
    Nhan_Dang_Mau_Sac_app()

elif menu == "🚗 Nhận dạng biển số xe":
    from Nhan_Dang_Bien_So_Xe.app import run as Nhan_Dang_Bien_So_Xe_app
    Nhan_Dang_Bien_So_Xe_app()

elif menu == "🖐 Nhận dạng cử chỉ tay":  
    from Nhan_Dang_Cu_Chi_Tay.app import run as Nhan_Dang_Cu_Chi_Tay_app
    Nhan_Dang_Cu_Chi_Tay_app()

elif menu == "🚦 Nhận dạng biển báo đường bộ":  
    from Nhan_Dang_Bien_Bao.app import run as Nhan_Dang_Bien_Bao_app
    Nhan_Dang_Bien_Bao_app()

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