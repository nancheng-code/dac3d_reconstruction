import numpy as np
from PIL import Image
import os


def load_multiband(paths):
    imgs = []

    for p in paths:
        if not os.path.exists(p):
            raise FileNotFoundError(f"文件不存在: {p}")

        img = Image.open(p).convert("RGB")
        img_arr = np.array(img, dtype=np.float32)
        gray = img_arr.mean(axis=2)
        imgs.append(gray)

    return np.stack(imgs, axis=2)


def load_default_apple():
    base = os.path.join(os.path.dirname(__file__), "..", "data")

    paths = [
        os.path.join(base, "apple_I_460.tif"),
        os.path.join(base, "apple_I_525.tif"),
        os.path.join(base, "apple_I_620.tif"),
    ]

    return load_multiband(paths)
