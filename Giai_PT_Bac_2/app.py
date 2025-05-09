import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

def gptb2(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                return 'Phương trình bậc 1 có vô số nghiệm'
            else:
                return 'Phương trình bậc 1 vô nghiệm'
        else:
            x = -c / b
            return f'Phương trình bậc 1 có nghiệm: x = {x:.2f}'
    else:
        delta = b**2 - 4*a*c
        if delta < 0:
            return 'Phương trình bậc 2 vô nghiệm'
        elif delta == 0:
            x = -b / (2*a)
            x = 0.0 if abs(x) < 1e-8 else x  
            return f'Phương trình bậc 2 có nghiệm kép: x = {x:.2f}'
        else:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            return f'Phương trình bậc 2 có nghiệm: x1 = {x1:.2f} và x2 = {x2:.2f}'

def ve_do_thi(a, b, c):
    x = np.linspace(-10, 10, 400)

    if a == 0:
        if b == 0 and c == 0:
            y = np.zeros_like(x)
            title = 'Phương trình có vô số nghiệm: Đường thẳng y = 0'
        elif b != 0:
            y = b * x + c
            title = f'Đồ thị hàm số bậc 1: y = {b}x + {c}'
        else:
            return None
    else:
        y = a * x**2 + b * x + c
        title = f'Đồ thị hàm số bậc 2: y = {a}x² + {b}x + {c}'

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, alpha=0.3)
    ax.plot(x, y, label=title, color='#1E88E5', linewidth=2.5)
    
    # Tìm giao điểm với trục Ox nếu có
    if a != 0 or b != 0:
        roots = []
        if a == 0 and b != 0:  # Bậc 1
            roots = [-c/b]
        elif a != 0:  # Bậc 2
            delta = b**2 - 4*a*c
            if delta >= 0:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                roots.append(x1)
                if delta > 0:
                    x2 = (-b - math.sqrt(delta)) / (2*a)
                    roots.append(x2)
        
        # Đánh dấu giao điểm
        for root in roots:
            if -10 <= root <= 10:  # Chỉ vẽ nếu giao điểm nằm trong phạm vi hiển thị
                ax.plot(root, 0, 'ro', markersize=8)
                ax.annotate(f'({root:.2f}, 0)', 
                           (root, 0), 
                           textcoords="offset points", 
                           xytext=(0,10), 
                           ha='center',
                           fontsize=9,
                           bbox=dict(boxstyle="round,pad=0.3", fc="#F8F9FA", ec="gray", alpha=0.8))
    
    # Thêm viền và tô màu nền cho đồ thị
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Thêm nhãn trục
    ax.set_xlabel('Trục x', fontsize=12)
    ax.set_ylabel('Trục y', fontsize=12)
    
    # Tiêu đề với phông và màu sắc đẹp hơn
    ax.set_title("Đồ thị hàm số", fontsize=14, fontweight='bold', color='#424242')
    
    # Tạo legend với viền
    legend = ax.legend(loc='upper right', fontsize=10, frameon=True)
    legend.get_frame().set_facecolor('#F8F9FA')
    legend.get_frame().set_edgecolor('gray')
    
    plt.tight_layout()
    return fig

def clear_input():
    st.session_state["nhap_a"] = 0.0
    st.session_state["nhap_b"] = 0.0
    st.session_state["nhap_c"] = 0.0

def run():
    # CSS tùy chỉnh cho giao diện
    st.markdown("""
    <style>
    .equation-header {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E0E0E0;
    }
    
    .equation-form {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .equation-display {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .result-section {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-top: 1rem;
    }
    
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Nút xóa với màu khác */
    .clear-button>button {
        background-color: #F44336;
    }
    
    .clear-button>button:hover {
        background-color: #D32F2F;
    }
    
    .input-label {
        font-weight: bold;
        color: #424242;
    }
    
    /* Tùy chỉnh input */
    .stNumberInput>div>div>input {
        border: 2px solid #E0E0E0;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #1E88E5;
        box-shadow: 0 0 0 2px rgba(30,136,229,0.2);
    }
    
    /* Tùy chỉnh màu nền chính */
    .main {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hiển thị tiêu đề và giới thiệu
    st.markdown('<div class="equation-header">🧮 Giải phương trình bậc 2: ax² + bx + c = 0</div>', unsafe_allow_html=True)
    
    # Hiển thị công thức toán học
    st.markdown("""
    <div class="equation-display">
        <b>Dạng tổng quát:</b> ax² + bx + c = 0<br>
        <b>Công thức delta:</b> Δ = b² - 4ac<br>
        <b>Nghiệm:</b><br>
        - Nếu Δ < 0: Phương trình vô nghiệm<br>
        - Nếu Δ = 0: x = -b/(2a)<br>
        - Nếu Δ > 0: x₁ = (-b + √Δ)/(2a) và x₂ = (-b - √Δ)/(2a)
    </div>
    """, unsafe_allow_html=True)

    # Form nhập liệu với thiết kế đẹp
    st.markdown('<div class="equation-form">', unsafe_allow_html=True)
    
    with st.form(key='columns_in_form', clear_on_submit=False):
        # Tiêu đề form
        st.markdown("<h3 style='text-align: center; color: #424242;'>Nhập hệ số phương trình</h3>", unsafe_allow_html=True)
        
        # Tạo 3 cột để nhập a, b, c
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<p class="input-label">Hệ số a:</p>', unsafe_allow_html=True)
            a = st.number_input('', key='nhap_a', value=0.0, step=0.1, format="%.1f", help="Nhập hệ số a của phương trình")
        
        with col2:
            st.markdown('<p class="input-label">Hệ số b:</p>', unsafe_allow_html=True)
            b = st.number_input('', key='nhap_b', value=0.0, step=0.1, format="%.1f", help="Nhập hệ số b của phương trình")
        
        with col3:
            st.markdown('<p class="input-label">Hệ số c:</p>', unsafe_allow_html=True)
            c = st.number_input('', key='nhap_c', value=0.0, step=0.1, format="%.1f", help="Nhập hệ số c của phương trình")
        
        # Hiển thị phương trình với các hệ số đã nhập
        if a == 0:
            if b == 0:
                eq_display = f"{c} = 0"
            else:
                if c == 0:
                    eq_display = f"{b}x = 0"
                elif c < 0:
                    eq_display = f"{b}x - {abs(c)} = 0"
                else:
                    eq_display = f"{b}x + {c} = 0"
        else:
            eq_display = f"{a}x² "
            if b != 0:
                if b > 0:
                    eq_display += f"+ {b}x"
                else:
                    eq_display += f"- {abs(b)}x"
            
            if c != 0:
                if c > 0:
                    eq_display += f" + {c}"
                else:
                    eq_display += f" - {abs(c)}"
            
            eq_display += " = 0"
        
        st.markdown(f"<div style='text-align: center; font-size: 1.2rem; margin: 1rem 0; padding: 0.5rem; background-color: white; border-radius: 5px; border: 1px solid #E0E0E0;'>{eq_display}</div>", unsafe_allow_html=True)
        
        # Nút giải và xóa trong 2 cột
        col1, col2 = st.columns(2)
        
        with col1:
            btn_giai = st.form_submit_button('Giải phương trình')
        
        with col2:
            st.markdown('<div class="clear-button">', unsafe_allow_html=True)
            btn_xoa = st.form_submit_button('Xóa dữ liệu', on_click=clear_input)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Kết quả
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    if 'nhap_a' in st.session_state or 'nhap_b' in st.session_state or 'nhap_c' in st.session_state:
        current_a = st.session_state.get('nhap_a', 0)
        current_b = st.session_state.get('nhap_b', 0)
        current_c = st.session_state.get('nhap_c', 0)
        
        if btn_giai:
            # Tính delta
            if current_a != 0:
                delta = current_b**2 - 4*current_a*current_c
                st.markdown(f"<p><b>Δ = b² - 4ac = {current_b}² - 4 × {current_a} × {current_c} = {delta:.2f}</b></p>", unsafe_allow_html=True)
            
            # Hiển thị kết quả
            s = gptb2(current_a, current_b, current_c)
            st.markdown(f'<h3>Kết quả:</h3>', unsafe_allow_html=True)
            st.markdown(f'<div style="background-color: white; padding: 1rem; border-radius: 5px; border-left: 3px solid #1E88E5;"><b>{s}</b></div>', unsafe_allow_html=True)
            
            # Vẽ đồ thị
            fig = ve_do_thi(current_a, current_b, current_c)
            if fig is not None:
                st.pyplot(fig)
        else:
            st.markdown('<h3>Kết quả:</h3><p>Nhấn nút "Giải phương trình" để xem kết quả.</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)