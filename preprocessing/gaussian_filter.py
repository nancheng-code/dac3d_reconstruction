import cv2
import numpy as np


def gaussian_denoise(image: np.ndarray,
                     ksize: int = 5,
                     sigma: float = 1.0) -> np.ndarray:
    """
    对三通道图像进行高斯滤波

    参数:
        image: (H, W, 3) float 或 uint8
        ksize: 高斯核大小 (必须为奇数)
        sigma: 高斯标准差

    返回:
        去噪后的图像
    """
    assert image.ndim == 3 and image.shape[2] == 3, "输入必须是三通道图像"

    filtered = np.zeros_like(image)

    for c in range(3):
        filtered[:, :, c] = cv2.GaussianBlur(
            image[:, :, c],
            (ksize, ksize),
            sigmaX=sigma,
            sigmaY=sigma
        )

    return filtered
