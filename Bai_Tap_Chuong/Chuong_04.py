import numpy as np
import cv2
import streamlit as st
from PIL import Image

L = 256

def run():
    st.subheader("📌 Các phép toán trong không gian tần số")

    option = st.selectbox("Chọn phép biến đổi:", [
        "🔍 Spectrum - Tính toán phổ ảnh",
        "⚙️ Frequency Filter - Lọc tần số ảnh",
        "🚫 Notch Reject Filter - Lọc Notch Reject",
        "🌊 Remove Moire - Loại bỏ Moire"
    ])

    uploaded_file = st.file_uploader("📤 Chọn ảnh grayscale", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img_pil = Image.open(uploaded_file).convert("L")  
        img_np = np.array(img_pil)
        imgout = np.zeros_like(img_np)

        if option == "🔍 Spectrum - Tính toán phổ ảnh":
            imgout = Spectrum(img_np)
        elif option == "⚙️ Frequency Filter - Lọc tần số ảnh":
            imgout = FrequencyFilter(img_np)
        elif option == "🚫 Notch Reject Filter - Lọc Notch Reject":
            imgout = DrawNotchRejectFilter()  
        elif option == "🌊 Remove Moire - Loại bỏ Moire":
            imgout = RemoveMoire(img_np)

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_np, caption="Ảnh gốc", use_column_width=True)
        with col2:
            st.image(imgout, caption="Ảnh sau biến đổi", use_column_width=True)

def Spectrum(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    # Bước 1 và 2: 
    # Tạo ảnh mới có kích thước PxQ
    # và thêm số 0 và phần mở rộng
    fp = np.zeros((P,Q), np.float64)
    fp[:M,:N] = imgin
    fp = fp/(L-1)

    # Bước 3:
    # Nhân (-1)^(x+y) để dời vào tâm ảnh
    for x in range(0, M):
        for y in range(0, N):
            if (x+y) % 2 == 1:
                fp[x,y] = -fp[x,y]

    # Bước 4:
    # Tính DFT    
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)

    # Tính spectrum
    S = np.sqrt(F[:,:,0]**2 + F[:,:,1]**2)
    S = np.clip(S, 0, L-1)
    S = S.astype(np.uint8)
    return S

def FrequencyFilter(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    # Bước 1 và 2: 
    # Tạo ảnh mới có kích thước PxQ
    # và thêm số 0 vào phần mở rộng
    fp = np.zeros((P,Q), np.float32)
    fp[:M,:N] = imgin

    # Bước 3:
    # Nhân (-1)^(x+y) để dời vào tâm ảnh
    for x in range(0, M):
        for y in range(0, N):
            if (x+y) % 2 == 1:
                fp[x,y] = -fp[x,y]
    # Bước 4:
    # Tính DFT    
    F = cv2.dft(fp, flags = cv2.DFT_COMPLEX_OUTPUT)

    # Bước 5: 
    # Tạo bộ lọc H thực High Pass Butterworth
    H = np.zeros((P,Q), np.float32)
    D0 = 60
    n = 2
    for u in range(0, P):
        for v in range(0, Q):
            Duv = np.sqrt((u-P//2)**2 + (v-Q//2)**2)
            if Duv > 0:
                H[u,v] = 1.0/(1.0 + np.power(D0/Duv,2*n))
    # Bước 6:
    # G = F*H nhân từng cặp
    G = F.copy()
    for u in range(0, P):
        for v in range(0, Q):
            G[u,v,0] = F[u,v,0]*H[u,v]
            G[u,v,1] = F[u,v,1]*H[u,v]
    
    # Bước 7:
    # IDFT
    g = cv2.idft(G, flags = cv2.DFT_SCALE)
    # Lấy phần thực
    gp = g[:,:,0]
    # Nhân với (-1)^(x+y)
    for x in range(0, P):
        for y in range(0, Q):
            if (x+y)%2 == 1:
                gp[x,y] = -gp[x,y]
    # Bước 8:
    # Lấy kích thước ảnh ban đầu
    imgout = gp[0:M,0:N]
    imgout = np.clip(imgout,0,L-1)
    imgout = imgout.astype(np.uint8)
    return imgout

def CreateNotchRejectFilter(P,Q):

    u1, v1 = 44, 58
    u2, v2 = 40, 119
    u3, v3 = 86, 59
    u4, v4 = 82, 119

    D0 = 10
    n = 2
    H = np.ones((P,Q), np.complex128)
    for u in range(0, P):
        for v in range(0, Q):
            h = 1.0
            # Bộ lọc u1, v1
            Duv = np.sqrt((u-u1)**2 + (v-v1)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u1))**2 + (v-(Q-v1))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0

            # Bộ lọc u2, v2
            Duv = np.sqrt((u-u2)**2 + (v-v2)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u2))**2 + (v-(Q-v2))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0

            # Bộ lọc u3, v3
            Duv = np.sqrt((u-u3)**2 + (v-v3)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u3))**2 + (v-(Q-v3))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0

            # Bộ lọc u4, v4
            Duv = np.sqrt((u-u4)**2 + (v-v4)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u4))**2 + (v-(Q-v4))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            H[u,v] = h
    return H

def DrawNotchRejectFilter():
    H = CreateNotchRejectFilter(250,180)
    H = H*(L-1)
    H = H.astype(np.uint8)
    return H
  
def RemoveMoire(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)

    # Zero-padding
    fp = np.zeros((P, Q), np.complex128)
    fp[:M, :N] = imgin

    # Shift to center
    fp *= (-1) ** np.fromfunction(lambda x, y: x + y, (P, Q))

    # DFT
    F = np.fft.fft2(fp)

    # Create and apply Notch Reject Filter
    H = CreateNotchRejectFilter(P, Q)  # Assuming CreateNotchRejectFilter is implemented
    G = F * H

    # IDFT
    g = np.fft.ifft2(G)

    # Shift back
    g *= (-1) ** np.fromfunction(lambda x, y: x + y, (P, Q))

    # Crop to the original size
    imgout = np.real(g[:M, :N])

    # Clip and convert to uint8
    imgout = np.clip(imgout, 0, 255).astype(np.uint8)

    return imgout