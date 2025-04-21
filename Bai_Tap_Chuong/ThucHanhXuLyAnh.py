import os
import joblib
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pytesseract
#import tensorflow
import cv2
import numpy as np
import sys
import os
import tensorflow as tf
from XuLyAnh import Chapter3 as c3

from XuLyAnh import Chapter04 as c4
from XuLyAnh import Chapter05 as c5
from XuLyAnh import Chapter9 as c9
import streamlit as st
from tkinter.filedialog import Open, SaveAs
import cv2
import numpy as np
import pandas as pd
from PIL import Image

@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img
#import ThucHanhXuLyAnh as codeChapter


# Hàm để cập nhật giá trị của imgin
def update_imgin(new_value):
    global imgin
    imgin = new_value
    




def onOpeningClosing():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c9.OpeningClosing(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))
def onOpeningClosing():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c9.OpeningClosing(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))
def onNegative():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.Negative(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))



def onLogarit():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.Logarit(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))
        # cv2.namedWindow("ImageOut", cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("ImageOut", imgout)

def onPower():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.Power(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))
        # cv2.namedWindow("ImageOut", cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("ImageOut", imgout)

def onPiecewiseLinear():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.PiecewiseLinear(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onHistogram():
        global imgout
        imgout = np.zeros((imgin.shape[0], 256, 3), np.uint8) + 255
        c3.Histogram(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onHistogramEqualization():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        # c3.HistogramEqualization(imgin,imgout)
        cv2.equalizeHist(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onLocalHistogram():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.LocalHistogram(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

        # cv2.namedWindow("ImageOut", cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("ImageOut", imgout)

def onHistogramStatistics():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.HistogramStatistics(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onSmoothing():
        global imgout
        imgout = c3.Smoothing(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onSmoothingGauss():
        global imgout
        imgout = c3.SmoothingGauss(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onMedianFilter():
        global imgout
        imgout = np.zeros(imgin.shape, np.uint8)
        c3.MedianFilter(imgin, imgout)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onSharpen():
        global imgout
        imgout = c3.Sharpen(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onUnSharpMasking():
        global imgout
        imgout = c3.UnSharpMasking(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onGradient():
        global imgout
        imgout = c3.Gradient(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

    #Chapter 4
        
def onSpectrum():
    global imgout
    imgout = c4.Spectrum(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onFrequencyFilter():
        global imgout
        imgout = c4.FrequencyFilter(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))
        

def onDrawFilter():
        global imgout
        imgout = c4.DrawNotchRejectFilter()
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onRemoveMoire():
        global imgout
        imgout = c4.RemoveMoire(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))   
        
#Chapter 5

def onCreateMotionNoise():
        global imgout
        imgout = c5.CreateMotionNoise(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))
        

def onDenoiseMotion():
        global imgout
        imgout = c5.DenoiseMotion(imgin)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onDenoisestMotion():
        global imgout
        temp = cv2.medianBlur(imgin, 7)
        imgout = c5.DenoiseMotion(temp)
        img_array = np.array(imgout)
        cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))


    #Chapter 9
def onErosion():
    global imgout
    imgout = c9.Erosion(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.IMREAD_GRAYSCALE))

def onDilation():
    imgout = c9.Dilation(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR))

def onBoundary():
    imgout = c9.Boundary(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR))

def onHoleFill():
    imgout = c9.HoleFill(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR))

def onMyConnectedComponent():
    imgout = c9.MyConnectedComponent(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR))

def onConnectedComponent():
    imgout = c9.ConnectedComponent(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR))

def onCountRice():
    imgout = c9.CountRice(imgin)
    img_array = np.array(imgout)
    cv2.imwrite('out1.jpg', cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR))