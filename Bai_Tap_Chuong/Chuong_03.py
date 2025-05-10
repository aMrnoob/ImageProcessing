import cv2
import numpy as np
import streamlit as st
from PIL import Image

L = 256

def run():
    st.subheader("📌 Các phép toán điểm ảnh")

    option = st.selectbox("Chọn phép biến đổi:", [
        "🎞 Negative - Chuyển đổi ảnh thành âm bản",
        "🔢 Logarit - Biến đổi logarit",
        "📊 Power (Gamma) - Biến đổi Gamma",
        "🔲 Piecewise Linear - Biến đổi theo đoạn tuyến tính",
        "📈 Histogram - Biểu đồ tần suất mức xám",
        "📏 Histogram Equalization - Bình phương tần số mức xám",
        "📊 Local Histogram - Tính toán biểu đồ tần suất theo vùng",
        "🌫 Gaussian Smoothing - Làm mịn với bộ lọc Gaussian",
        "🔪 Sharpening - Làm sắc nét ảnh",
        "🖼 Unsharp Masking - Phương pháp làm sắc nét ngược",
        "🛠 Median Filter - Bộ lọc trung bình",
        "⚡ Gradient - Tính toán gradient ảnh"
    ], index=0)

    uploaded_file = st.file_uploader("📤 Chọn ảnh grayscale", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img_pil = Image.open(uploaded_file).convert("L") 
        img_np = np.array(img_pil)
        imgout = np.zeros_like(img_np)

        if option == "🎞 Negative - Chuyển đổi ảnh thành âm bản":
            Negative(img_np, imgout)
        elif option == "🔢 Logarit - Biến đổi logarit":
            Logarit(img_np, imgout)
        elif option == "📊 Power (Gamma) - Biến đổi Gamma":
            Power(img_np, imgout)
        elif option == "🔲 Piecewise Linear - Biến đổi theo đoạn tuyến tính":
            PiecewiseLinear(img_np, imgout)
        elif option == "📈 Histogram - Biểu đồ tần suất mức xám":
            Histogram(img_np, imgout)
        elif option == "📏 Histogram Equalization - Bình phương tần số mức xám":
            HistogramEqualization(img_np, imgout)
        elif option == "📊 Local Histogram - Tính toán biểu đồ tần suất theo vùng":
            LocalHistogram(img_np, imgout)
        elif option == "🔵 Smoothing - Làm mịn ảnh":
            imgout = MySmoothing(img_np, imgout)
        elif option == "🌫 Gaussian Smoothing - Làm mịn với bộ lọc Gaussian":
            imgout = SmoothingGauss(img_np)
        elif option == "🔪 Sharpening - Làm sắc nét ảnh":
            imgout = Sharpen(img_np)
        elif option == "🖼 Unsharp Masking - Phương pháp làm sắc nét ngược":
            imgout = UnSharpMasking(img_np)
        elif option == "🛠 Median Filter - Bộ lọc trung bình":
            MedianFilter(img_np, imgout)
        elif option == "⚡ Gradient - Tính toán gradient ảnh":
            imgout = Gradient(img_np)

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_np, caption="Ảnh gốc", use_container_width=True)
        with col2:
            st.image(imgout, caption="Ảnh sau biến đổi", use_container_width=True)

def Negative(imgin, imgout):
    M, N = imgin.shape
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            s = L - 1 - r
            imgout[x, y] = s


def Logarit(imgin, imgout):
    M, N = imgin.shape
    c = (L - 1) / np.log(L)

    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            if r == 0:
                r = 1
            s = c * np.log(1.0 + r)
            imgout[x, y] = s.astype(np.uint8)


def Power(imgin, imgout):
    M, N = imgin.shape
    gamma = 5.0
    c = np.power(L - 1, 1 - gamma)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            s = c * np.power(r, gamma)
            imgout[x, y] = s.astype(np.uint8)


def PiecewiseLinear(imgin, imgout):
    M, N = imgin.shape
    rmin, rmax, rminloc, rmaxloc = cv2.minMaxLoc(imgin)
    r1 = rmin
    if rmin == 0:
        r1 = 1
    s1 = 0
    r2 = rmax
    if rmax == L - 1:
        r2 = L - 2
    s2 = L - 1
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            if r < r1:
                s = s1 / r1 * r
            elif r < r2:
                s = (s2 - s1) / (r2 - r1) * (r - r1) + s1
            else:
                s = (L - 1 - s2) / (L - 1 - r2) * (r - r2) + s2
            imgout[x, y] = s.astype(np.uint8)


def Histogram(imgin, imgout):
    M, N = imgin.shape
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r] + 1

    p = np.zeros(L, np.float64)
    for r in range(0, L):
        p[r] = h[r] / (M * N)

    scale = 1200
    for r in range(0, L):
        cv2.line(imgout, (r, M - 1), (r, M - 1 - (int)(scale * p[r])), (255, 255, 0))
    return


def HistogramEqualization(imgin, imgout):
    M, N = imgin.shape
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r] + 1

    p = np.zeros(L, np.float32)
    for r in range(0, L):
        p[r] = h[r] / (M * N)

    s = np.zeros(L, np.float32)
    for k in range(0, L):
        for j in range(0, k + 1):
            s[k] = s[k] + p[j]
        s[k] = s[k] * (L - 1)

    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            imgout[x, y] = s[r].astype(np.uint8)


def LocalHistogram(imgin, imgout):
    M, N = imgin.shape
    m = 3
    n = 3
    a = m // 2
    b = n // 2
    w = np.zeros((m, n), np.uint8)
    for x in range(a, M - a):
        for y in range(b, N - b):
            for s in range(-a, a + 1):
                for t in range(-b, b + 1):
                    w[s + a, t + b] = imgin[x + s, y + t]
            cv2.equalizeHist(w, w)
            imgout[x, y] = w[a, b]


def HistogramStatistics(imgin, imgout):
    M, N = imgin.shape
    [mG, sigmaG] = cv2.meanStdDev(imgin)
    m = 3
    n = 3
    a = m // 2
    b = n // 2
    w = np.zeros((m, n), np.uint8)
    C = 22.8
    k0 = 0.0
    k1 = 0.1
    k2 = 0.0
    k3 = 0.1
    for x in range(a, M - a):
        for y in range(b, N - b):
            for s in range(-a, a + 1):
                for t in range(-b, b + 1):
                    w[s + a, t + b] = imgin[x + s, y + t]
            [msxy, sigmasxy] = cv2.meanStdDev(w)
            if (k0 * mG <= msxy and msxy <= k1 * mG) and (k2 * sigmaG <= sigmasxy and sigmasxy <= k3 * sigmaG):
                imgout[x, y] = (C * imgin[x, y]).astype(np.uint8)
            else:
                imgout[x, y] = imgin[x, y]
    return


def MySmoothing(imgin, imgout):
    M, N = imgin.shape
    m = 11
    n = 11
    a = m // 2
    b = m // 2
    w = np.ones((m, n), np.float32) / (m * n)
    for x in range(a, M - a):
        for y in range(b, N - b):
            res = 0.0
            for s in range(-a, a + 1):
                for t in range(-b, b + 1):
                    res = res + w[s + a, t + b] * imgin[x + s, y + t]
            imgout[x, y] = res.astype(np.uint8)


def Smoothing(imgin):
    M, N = imgin.shape
    m = 21
    n = 21
    a = m // 2
    b = m // 2
    w = np.ones((m, n), np.int32) / (m * n)
    imgout = cv2.filter2D(imgin, cv2.CV_8UC1, w)
    imgout = cv2.blur(imgin, (m,n))
    return imgout


def SmoothingGauss(imgin):
    M, N = imgin.shape
    m = 51
    n = 51
    a = m // 2
    b = m // 2
    sigma = 7.0
    w = np.zeros((m, n), np.int32)
    for s in range(-a, a + 1):
        for t in range(-b, b + 1):
            w[s + a, t + b] = np.exp(-(s * s + t * t) / (2 * sigma * sigma))
    sum = np.sum(w)
    w = w / sum
    imgout = cv2.filter2D(imgin, cv2.CV_8UC1, w)
    # imgout = cv2.GaussianBlur(imgin, (m,n), 7.0)
    return imgout


def MySort(w):
    m, n = w.shape
    w = np.reshape(w, m * n)
    w = np.sort(w)
    return w[m * n // 2]


def MedianFilter(imgin, imgout):
    M, N = imgin.shape
    m = 5
    n = 5
    a = m // 2
    b = n // 2
    w = np.zeros((m, n), np.uint8)
    for x in range(a, M - a):
        for y in range(b, N - b):
            for s in range(-a, a + 1):
                for t in range(-b, b + 1):
                    w[s + a, t + b] = imgin[x + s, y + t]
            r = MySort(w)
            imgout[x, y] = r


def MySharpen(imgin, imgout):
    M, N = imgin.shape
    m = 3
    n = 3
    a = m // 2
    b = m // 2
    w = np.zeros((m, n), np.int32)
    w[0, 0] = 1
    w[0, 1] = 1
    w[0, 2] = 1
    w[1, 0] = 1
    w[1, 1] = -8
    w[1, 2] = 1
    w[2, 0] = 1
    w[2, 1] = 1
    w[2, 2] = 1
    for x in range(a, M - a):
        for y in range(b, N - b):
            r = 0
            for s in range(-a, a + 1):
                for t in range(-b, b + 1):
                    r = r + w[s + a, t + b] * imgin[x + s, y + t]
            r = imgin[x, y] - r;
            if r < 0:
                r = 0
            if r > L - 1:
                r = L - 1
            imgout[x, y] = r


def Sharpen(imgin):
    w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], np.int32)
    temp = cv2.filter2D(imgin, cv2.CV_32FC1, w)
    result = imgin - temp
    result = np.clip(result, 0, L - 1)
    imgout = result.astype(np.uint8)
    return imgout


def UnSharpMasking(imgin):
    blur = cv2.GaussianBlur(imgin, (3, 3), 1.0).astype(np.float64)
    mask = imgin - blur
    k = 10.0
    imgout = imgin + k * mask
    imgout = np.clip(imgout, 0, L - 1).astype(np.uint8)
    return imgout


def MyGradient(imgin, imgout):
    M, N = imgin.shape
    wx = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], np.int32)
    wy = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.int32)
    m = 3
    n = 3
    a = m // 2
    b = m // 2
    for x in range(a, M - a):
        for y in range(b, N - b):
            gx = 0
            gy = 0
            for s in range(-a, a + 1):
                for t in range(-b, b + 1):
                    gx = gx + wx[s + a, t + b] * imgin[x + s, y + t]
                    gy = gy + wy[s + a, t + b] * imgin[x + s, y + t]
            g = abs(gx) + abs(gy)
            if g < 0:
                g = 0
            if g > L - 1:
                g = L - 1
            imgout[x, y] = g


def Gradient(imgin):
    wx = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], np.int32)
    wy = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.int32)
    gx = cv2.filter2D(imgin, cv2.CV_32FC1, wx);
    gy = cv2.filter2D(imgin, cv2.CV_32FC1, wy);
    g = abs(gx) + abs(gy)
    imgout = np.clip(g, 0, L - 1).astype(np.uint8)
    return imgout
