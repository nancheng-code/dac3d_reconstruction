import numpy as np
import cv2
import os
from PIL import Image

from preprocessing.image_loader import load_default_apple


def register_multiband(img, motion=cv2.MOTION_TRANSLATION):
    """
    多通道图像配准
    使用 ECC (Enhanced Correlation Coefficient)

    :param img: HxWxC
    :param motion: 运动模型
    :return: 配准后图像
    """

    C = img.shape[2]
    ref = img[:, :, 0].astype(np.uint8)

    registered = np.zeros_like(img)
    registered[:, :, 0] = ref

    for i in range(1, C):
        moving = img[:, :, i].astype(np.uint8)

        warp = np.eye(2, 3, dtype=np.float32)

        try:
            criteria = (
                cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                50,
                1e-6
            )

            _, warp = cv2.findTransformECC(
                ref,
                moving,
                warp,
                motion,
                criteria
            )

            aligned = cv2.warpAffine(
                moving,
                warp,
                (moving.shape[1], moving.shape[0]),
                flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
            )

            registered[:, :, i] = aligned

        except cv2.error:
            print(f"⚠ 通道 {i} 配准失败，保留原图")
            registered[:, :, i] = moving

    return registered


def save_registered(img, name="registered.tif"):
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    os.makedirs(out_dir, exist_ok=True)

    path = os.path.join(out_dir, name)
    Image.fromarray(img.astype(np.uint8)).save(path)

    print("✅ 已保存:", path)


if __name__ == "__main__":
    print("读取图像...")
    img = load_default_apple()

    print("执行图像配准...")
    reg = register_multiband(img)

    save_registered(reg)

    print("图像配准完成")
