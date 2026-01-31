import numpy as np
from .image_loader import load_default_apple
from .background_correction import dark_field_correction
from .image_registration import register_multiband
import cv2


def run_preprocessing():
    """
    完整的三通道图像预处理 pipeline:
    1. 读取默认图像
    2. 暗场校正
    3. 图像配准
    4. 高斯滤波去噪
    """
    print("读取图像...")
    img = load_default_apple()  # HxWx3, dtype=np.uint8

    print("暗场校正...")
    img_corrected = dark_field_correction(img)

    print("图像配准...")
    img_registered = register_multiband(img_corrected)

    print("高斯滤波去噪...")
    img_denoised = np.zeros_like(img_registered)
    for i in range(img_registered.shape[2]):
        img_denoised[:, :, i] = cv2.GaussianBlur(img_registered[:, :, i], (3, 3), 0)

    print("预处理完成")
    return img_denoised
