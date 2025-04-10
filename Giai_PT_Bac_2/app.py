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

    fig, ax = plt.subplots()
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
    ax.grid(True)
    ax.plot(x, y, label=title, color='red')
    ax.legend()
    ax.set_title("Đồ thị hàm số")
    return fig


def clear_input():
    st.session_state["nhap_a"] = 0.0
    st.session_state["nhap_b"] = 0.0
    st.session_state["nhap_c"] = 0.0

def run():
    st.subheader('🧮 Giải phương trình bậc 2')

    with st.form(key='columns_in_form', clear_on_submit=False):
        a = st.number_input('Nhập a', key='nhap_a')
        b = st.number_input('Nhập b', key='nhap_b')
        c = st.number_input('Nhập c', key='nhap_c')
        col1, col2 = st.columns(2)

        with col1:
            btn_giai = st.form_submit_button('Giải')
        with col2:
            btn_xoa = st.form_submit_button('Xóa', on_click=clear_input)

        if btn_giai:
            s = gptb2(a, b, c)
            st.markdown(f'**Kết quả:** {s}')
            fig = ve_do_thi(a, b, c)
            if fig is not None:
                st.pyplot(fig)

        else:
            st.markdown('**Kết quả:**')
