import cv2
import numpy as np
import streamlit as st
from PIL import Image

L = 256
imgin = None
imgout = None

def run():
    st.subheader("📌 Các phép toán trong xử lý ảnh nhị phân")

    option = st.selectbox("Chọn phép biến đổi:", [
        "➖ Erosion - Co thắt ảnh",
        "➕ Dilation - Phóng đại ảnh",
        "🔄 Opening/Closing - Mở rộng/Đóng ảnh",
        "🔲 Boundary - Biên ảnh",
        "🕳️ Hole Fill - Lấp đầy lỗ",
        "🔗 My Connected Component - Thành phần liên thông tự tạo",
        "🔍 Connected Component - Thành phần liên thông",
        "🌾 Count Rice - Đếm hạt gạo"
    ])

    uploaded_file = st.file_uploader("📤 Chọn ảnh nhị phân", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img_pil = Image.open(uploaded_file).convert("L")  
        img_np = np.array(img_pil)
        imgout = np.zeros_like(img_np)

        if option == "➖ Erosion - Co thắt ảnh":
            imgout = Erosion(img_np)
        elif option == "➕ Dilation - Phóng đại ảnh":
            imgout = Dilation(img_np)
        elif option == "🔄 Opening/Closing - Mở rộng/Đóng ảnh":
            imgout = OpeningClosing(img_np, imgout)
        elif option == "🔲 Boundary - Biên ảnh":
            imgout = Boundary(img_np)
        elif option == "🕳️ Hole Fill - Lấp đầy lỗ":
            imgout = HoleFill(img_np)
        elif option == "🔗 My Connected Component - Thành phần liên thông tự tạo":
            imgout = MyConnectedComponent(img_np)
        elif option == "🔍 Connected Component - Thành phần liên thông":
            imgout = ConnectedComponent(img_np)
        elif option == "🌾 Count Rice - Đếm hạt gạo":
            imgout = CountRice(img_np)

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_np, caption="Ảnh gốc", use_column_width=True)
        with col2:
            st.image(imgout, caption="Ảnh sau biến đổi", use_column_width=True)

def Erosion(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 45))
    return cv2.erode(imgin, w)

def Dilation(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.dilate(imgin, w)

def OpeningClosing(imgin, imgout):
    w = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    temp = cv2.morphologyEx(imgin, cv2.MORPH_OPEN, w)
    cv2.morphologyEx(temp, cv2.MORPH_CLOSE, w, imgout)

def Boundary(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    temp = cv2.erode(imgin, w)
    return imgin - temp

def HoleFill(imgin):
    imgout = imgin.copy()
    M, N = imgout.shape
    mask = np.zeros((M+2, N+2), np.uint8)
    cv2.floodFill(imgout, mask, (105, 297), L-1)
    return imgout

def MyConnectedComponent(imgin):
    ret, temp = cv2.threshold(imgin, 200, L-1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    M, N = temp.shape
    dem = 0
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            if temp[x, y] == L-1:
                mask = np.zeros((M+2, N+2), np.uint8)
                cv2.floodFill(temp, mask, (y, x), (color, color, color))
                dem += 1
                color += 1
    print('Co %d thanh phan lien thong' % dem)
    a = np.zeros(L, np.int64)
    for x in range(0, M):
        for y in range(0, N):
            r = temp[x, y]
            if r > 0:
                a[r] += 1
    dem = 1
    for r in range(0, L):
        if a[r] > 0:
            print('%4d   %5d' % (dem, a[r]))
            dem += 1
    return temp

def ConnectedComponent(imgin):
    ret, temp = cv2.threshold(imgin, 200, L-1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    dem, label = cv2.connectedComponents(temp)
    print('Co %d thanh phan lien thong' % (dem-1))
    a = np.zeros(dem, np.int64)
    M, N = label.shape
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            a[r] += 1
            if r > 0:
                label[x, y] += color
    for r in range(1, dem):
        print('%4d %10d' % (r, a[r]))
    return label.astype(np.uint8)

def CountRice(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81))
    temp = cv2.morphologyEx(imgin, cv2.MORPH_TOPHAT, w)
    ret, temp = cv2.threshold(temp, 100, L-1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    temp = cv2.medianBlur(temp, 3)
    dem, label = cv2.connectedComponents(temp)
    print('Co %d hat gao' % dem)
    a = np.zeros(dem, np.int64)
    M, N = label.shape
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            a[r] += 1
            if r > 0:
                label[x, y] += color
    for r in range(0, dem):
        print('%4d %10d' % (r, a[r]))

    max_val = a[1]
    rmax = 1
    for r in range(2, dem):
        if a[r] > max_val:
            max_val = a[r]
            rmax = r

    xoa = np.array([], np.int64)
    for r in range(1, dem):
        if a[r] < 0.5 * max_val:
            xoa = np.append(xoa, r)

    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            if r > 0:
                r -= color
                if r in xoa:
                    label[x, y] = 0
    return label.astype(np.uint8)
