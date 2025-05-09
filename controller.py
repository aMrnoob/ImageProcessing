import streamlit as st
from PIL import Image
import time
import base64
from streamlit_lottie import st_lottie
import json
import requests

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Xử lý ảnh số",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh
def add_custom_css():
    st.markdown("""
    <style>
        /* Gradient background cho toàn trang */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Card style cho các section */
        .card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }
        
        /* Header style */
        .header {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Button style */
        .stButton > button {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Category button style */
        .category-btn {
            display: block;
            width: 100%;
            text-align: left;
            padding: 12px 15px;
            background-color: white;
            border-radius: 8px;
            margin-bottom: 10px;
            border: none;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            font-weight: 500;
            color: #333;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .category-btn:hover {
            background: linear-gradient(90deg, #e9f0ff 0%, #d4e4ff 100%);
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            cursor: pointer;
        }
        
        .category-btn.active {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar style */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
        }
        
        /* Tabs style */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            height: auto;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: white !important;
        }
        
        /* Animation style */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.8s ease forwards;
        }
        
        /* Footer style */
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            margin-top: 50px;
            border-top: 1px solid #ddd;
        }
        
        /* Badge style */
        .badge {
            display: inline-block;
            padding: 5px 10px;
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: white;
            border-radius: 15px;
            font-size: 15px;
            margin-right: 5px;
        }
        
        /* Responsive layout */
        @media screen and (max-width: 768px) {
            .card {
                padding: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Lưu trạng thái active menu
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "🧮 Giải phương trình bậc 2"

if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = "Chương 3: Các phép toán điểm ảnh"

# Function để lấy animation Lottie
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Animation cho các chức năng
lottie_url = "https://assets6.lottiefiles.com/packages/lf20_fcfjwiyb.json"
lottie_json = load_lottieurl(lottie_url)

# Header với logo và thông tin
st.markdown('<div class="header fade-in">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    try:
        logo = Image.open("C:/Users/Admin/Documents/Github/ImageProcessing/ImageProcessing/logo_ute.png")
        st.image(logo, width=120)
    except:
        st.warning("Không thể tải logo. Vui lòng kiểm tra đường dẫn.")

with col2:
    st.markdown("""
        <div style='font-size: 20px; font-weight: bold; line-height: 1.6;'>
            👨‍🏫 <b>Giảng viên phụ trách:</b> thầy Trần Tiến Đức<br>
            📚 <b>Bộ môn:</b> Xử lý ảnh số<br>
            🏫 <b>Trường:</b> Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh
        </div>
        <br>
        <div style='font-size: 22px; line-height: 1.9;'>
            👥 <b>Thành viên nhóm:</b><br>
            <div class="badge">▪️ Tô Hữu Đức – 22110311</div>
            <div class="badge">▪️ Đỗ Văn Thường – 22110432</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Animation cho sidebar
if lottie_json:
    with st.sidebar:
        st_lottie(lottie_json, height=180, key="sidebar_animation")

# Sidebar danh mục
st.sidebar.markdown('<h2 style="text-align: center;">📚 Danh mục chức năng</h2>', unsafe_allow_html=True)

# Danh sách các chức năng
menu_items = [
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

# SỬA: Sử dụng button thật của streamlit thay vì HTML button
for item in menu_items:
    button_key = f"menu_button_{menu_items.index(item)}"
    if st.sidebar.button(item, key=button_key, 
                         help=f"Mở chức năng {item}", 
                         use_container_width=True,
                         type="primary" if st.session_state.current_menu == item else "secondary"):
        st.session_state.current_menu = item
        # Reset chapter khi chuyển sang menu mới
        if item != "📝 Bài tập chương":
            st.session_state.current_chapter = "Chương 3: Các phép toán điểm ảnh"
        st.rerun()

# Nếu chọn Bài tập chương, hiển thị danh sách chương
if st.session_state.current_menu == "📝 Bài tập chương":
    st.sidebar.markdown('<h3 style="margin-top: 30px;">📖 Chọn chương</h3>', unsafe_allow_html=True)
    
    chapters = [
        "Chương 3: Các phép toán điểm ảnh",
        "Chương 4: Các phép toán không gian",
        "Chương 9: Xử lý ảnh hình thái"
    ]
    
    # SỬA: Sử dụng button thật của streamlit cho chapters
    for chapter in chapters:
        chapter_key = f"chapter_button_{chapters.index(chapter)}"
        if st.sidebar.button(chapter, key=chapter_key, 
                            help=f"Mở {chapter}", 
                            use_container_width=True,
                            type="primary" if st.session_state.current_chapter == chapter else "secondary"):
            st.session_state.current_chapter = chapter
            st.rerun()

# Phần nội dung chính
st.markdown(f'<div class="card fade-in"><h1 style="text-align: center;">🧠 Ứng dụng Xử lý Ảnh Số</h1></div>', unsafe_allow_html=True)

# Hiển thị module tương ứng
try:
    with st.container():
        st.markdown(f'<div class="card fade-in">', unsafe_allow_html=True)
        
        # Hiển thị tiêu đề của module đang chọn
        st.subheader(f"Module: {st.session_state.current_menu}")
        
        # Hiệu ứng loading
        with st.spinner(f"Đang tải module {st.session_state.current_menu}..."):
            time.sleep(0.5)  # Hiệu ứng loading ngắn
            
            if st.session_state.current_menu == "🧮 Giải phương trình bậc 2":
                from Giai_PT_Bac_2.app import run as Giai_PT_Bac_2_app
                Giai_PT_Bac_2_app()
                
            elif st.session_state.current_menu == "🎭 Nhận dạng khuôn mặt":
                from Nhan_Dang_Khuon_Mat.app import run as Nhan_Dang_Khuon_Mat_app
                Nhan_Dang_Khuon_Mat_app()
                
            elif st.session_state.current_menu == "😊 Nhận dạng cảm xúc":
                from Nhan_Dang_Cam_Xuc.app import run as Nhan_Dang_Cam_Xuc_app
                Nhan_Dang_Cam_Xuc_app()
                
            elif st.session_state.current_menu == "👁️ Nhận dạng đối tượng":
                from Nhan_Dang_Doi_Tuong.app import run as Nhan_Dang_Doi_Tuong_app
                Nhan_Dang_Doi_Tuong_app()
                
            elif st.session_state.current_menu == "🍎 Nhận dạng trái cây":
                from Nhan_Dang_Trai_Cay.app import run as Nhan_Dang_Trai_Cay_app
                Nhan_Dang_Trai_Cay_app()
                
            elif st.session_state.current_menu == "🔢 Nhận dạng chữ số":
                from Nhan_Dang_Chu_So.app import run as Nhan_Dang_Chu_So_app
                Nhan_Dang_Chu_So_app()
                
            elif st.session_state.current_menu == "🎨 Nhận dạng màu sắc":
                from Nhan_Dang_Mau_Sac.app import run as Nhan_Dang_Mau_Sac_app
                Nhan_Dang_Mau_Sac_app()
                
            elif st.session_state.current_menu == "🚗 Nhận dạng biển số xe":
                from Nhan_Dang_Bien_So_Xe.app import run as Nhan_Dang_Bien_So_Xe_app
                Nhan_Dang_Bien_So_Xe_app()
                
            elif st.session_state.current_menu == "🖐 Nhận dạng cử chỉ tay":
                from Nhan_Dang_Cu_Chi_Tay.app import run as Nhan_Dang_Cu_Chi_Tay_app
                Nhan_Dang_Cu_Chi_Tay_app()
                
            elif st.session_state.current_menu == "🚦 Nhận dạng biển báo đường bộ":
                from Nhan_Dang_Bien_Bao.app import run as Nhan_Dang_Bien_Bao_app
                Nhan_Dang_Bien_Bao_app()
                
            elif st.session_state.current_menu == "📝 Bài tập chương":
                # Hiển thị module tương ứng với chương được chọn
                if st.session_state.current_chapter == "Chương 3: Các phép toán điểm ảnh":
                    from Bai_Tap_Chuong.Chuong_03 import run as Chuong_3_app
                    Chuong_3_app()
                    
                elif st.session_state.current_chapter == "Chương 4: Các phép toán không gian":
                    from Bai_Tap_Chuong.Chuong_04 import run as Chuong_4_app
                    Chuong_4_app()
                    
                elif st.session_state.current_chapter == "Chương 9: Xử lý ảnh hình thái":
                    from Bai_Tap_Chuong.Chuong_09 import run as Chuong_9_app
                    Chuong_9_app()
                    
                else:
                    st.info("Vui lòng chọn một chương từ menu bên trái.")
            
        st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Có lỗi xảy ra: {e}")
    st.info("Đường dẫn module có thể không chính xác hoặc module chưa được cài đặt.")

# Footer
st.markdown("""
<div class="footer fade-in">
    <p>© 2025 Nhóm Xử lý ảnh số - Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh</p>
    <p>Phiên bản: 99.99.99.99.99.99</p>
</div>
""", unsafe_allow_html=True)

# Thêm nút back-to-top
st.markdown("""
<script>
    // JavaScript để thêm nút back-to-top
    window.onscroll = function() {
        scrollFunction()
    };

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("backToTopBtn").style.display = "block";
        } else {
            document.getElementById("backToTopBtn").style.display = "none";
        }
    }

    function topFunction() {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    }
</script>
""", unsafe_allow_html=True)