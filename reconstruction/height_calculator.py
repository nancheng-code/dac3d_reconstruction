import numpy as np
from scipy.interpolate import LinearNDInterpolator
from PIL import Image
import os

from preprocessing.preprocessing_pipeline import run_preprocessing


class HeightCalculator:
    def __init__(self, lut_path):
        # 1️⃣ 加载字典型 LUT
        self.lut = np.load(lut_path, allow_pickle=True).item()
        delta1_grid = self.lut['delta1']
        delta2_grid = self.lut['delta2']
        Z_grid = self.lut['z']

        # 2️⃣ 构建二维查表插值器
        from scipy.interpolate import RegularGridInterpolator
        self.interp = RegularGridInterpolator(
            (delta1_grid, delta2_grid),
            Z_grid,
            bounds_error=False,  # 超出范围返回 fill_value
            fill_value=np.nan
        )

        print(f"LUT 已加载: {lut_path}")

    def compute_height_map(self, image):
        """
        image: HxWx3 三通道图像 (I_460, I_525, I_620)
        """
        assert image.ndim == 3 and image.shape[2] == 3, "输入必须是三通道图像"

        delta1 = image[:, :, 1] - image[:, :, 0]  # I_525 - I_460
        delta2 = image[:, :, 2] - image[:, :, 1]  # I_620 - I_525

        # 查表
        H, W = delta1.shape
        points = np.stack([delta1.ravel(), delta2.ravel()], axis=-1)  # (H*W, 2)
        height_map_flat = self.interp(points)
        height_map = height_map_flat.reshape(H, W)

        # 标记无效点：饱和点
        mask_saturated = np.max(image, axis=2) >= 255
        height_map[mask_saturated] = np.nan

        return height_map

    def save_height_map(self, height_map, out_name="height_map.tif"):
        out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, out_name)

        # 保存为 32-bit TIFF
        im = Image.fromarray(np.nan_to_num(height_map).astype(np.float32))
        im.save(path)
        print("高度图已保存:", path)


if __name__ == "__main__":
    # 1️⃣ 获取预处理后的图像
    img = run_preprocessing()

    # 2️⃣ 加载 ARC LUT
    lut_path = os.path.join(os.path.dirname(__file__), "apple_lut.npy")
    hc = HeightCalculator(lut_path)

    # 3️⃣ 计算高度图
    height_map = hc.compute_height_map(img)

    # 4️⃣ 保存高度图
    hc.save_height_map(height_map, "apple_height_map.tif")

    import numpy as np

    # 假设 height_map 是你的高度图 (HxW)
    num_nan = np.sum(np.isnan(height_map))
    total_pixels = height_map.size

    print(f"高度图总像素数: {total_pixels}")
    print(f"NaN 像素数: {num_nan}")
    print(f"NaN 占比: {num_nan / total_pixels * 100:.2f}%")

