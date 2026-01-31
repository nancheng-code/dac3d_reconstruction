import numpy as np
import os
from PIL import Image
from preprocessing.image_loader import load_default_apple


def estimate_background(img):
    """
    估计背景（每个通道最小值）
    :param img: HxWxC
    :return: 1x1xC background
    """
    return img.min(axis=(0, 1))


def dark_field_correction(img, background=None):
    """
    暗场校正
    :param img: 原始多通道图像
    :param background: 背景（可选）
    :return: 校正后图像
    """
    if background is None:
        background = estimate_background(img)

    corrected = img - background
    corrected = np.clip(corrected, 0, 255)

    return corrected


def save_image(img, name="background_corrected.tif"):
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    os.makedirs(out_dir, exist_ok=True)

    path = os.path.join(out_dir, name)
    Image.fromarray(img.astype(np.uint8)).save(path)

    print("✅ 已保存:", path)


if __name__ == "__main__":
    print("读取图像...")
    img = load_default_apple()

    print("执行暗场校正...")
    corrected = dark_field_correction(img)

    save_image(corrected)

    print("背景校正完成")
