import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras import datasets
import numpy as np
import random

def tao_anh_ngau_nhien():
    image = np.zeros((10*28, 10*28), np.uint8)
    data = np.zeros((100,28,28,1), np.uint8)

    for i in range(0, 100):
        n = random.randint(0, 9999)
        sample = st.session_state.X_test[n]
        data[i] = sample
        x = i // 10
        y = i % 10
        image[x*28:(x+1)*28,y*28:(y+1)*28] = sample[:,:,0]    
    return image, data

def run():
    st.title("🔢 Nhận dạng chữ số MNIST")

    if 'is_load' not in st.session_state:
        model = model_from_json(open('Nhan_Dang_Chu_So/model/digit_config.json').read())
        model.load_weights('Nhan_Dang_Chu_So/model/digit_weight.h5')

        model.compile(
            loss="categorical_crossentropy",
            optimizer=tf.keras.optimizers.Adam(),
            metrics=["accuracy"]
        )
        st.session_state.model = model

        (_, _), (X_test, _) = datasets.mnist.load_data()
        X_test = X_test.reshape((10000, 28, 28, 1))
        st.session_state.X_test = X_test

        st.session_state.is_load = True

    col1, col2 = st.columns([1.2, 1])  

    with col1:
        if st.button('Tạo ảnh'):
            image, data = tao_anh_ngau_nhien()
            st.session_state.image = image
            st.session_state.data = data

        if 'image' in st.session_state:
            st.image(
                st.session_state.image,
                caption="Ảnh ngẫu nhiên",
                use_container_width=True,
                output_format="PNG"
            )

    with col2:
        if 'image' in st.session_state:
            if st.button('Nhận dạng'):
                data = st.session_state.data / 255.0
                data = data.astype('float32')
                ket_qua = st.session_state.model.predict(data)

                so_list = [str(np.argmax(x)) for x in ket_qua]
                s = " ".join(" ".join(so_list[i:i+10]) for i in range(0, 100, 10))

                st.markdown(f"""
                    <div style="font-size: 37px; font-family: 'Courier New', monospace; padding-left: 1.5rem; background-color: #262730; color: white; border-radius: 8px; line-height: 1.53;">
                        <p>{s}</p>
                    </div> """, unsafe_allow_html=True)



