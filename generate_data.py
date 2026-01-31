import os
from PIL import Image
import numpy as np

# 输入输出路径
input_path = "apple.jpg"
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# 打开图片
img = Image.open(input_path).convert("RGB")
img_array = np.array(img, dtype=np.float32)

# 模拟不同波长的光谱响应
# 这里使用近似线性加权RGB通道生成波段图像
# I_460 -> 蓝色主导
# I_525 -> 绿色主导
# I_620 -> 红色主导
wavelengths = {
    "460": [0.1, 0.3, 1.0],  # 蓝色增强
    "525": [0.2, 1.0, 0.2],  # 绿色增强
    "620": [1.0, 0.3, 0.2],  # 红色增强
}

for wl, weights in wavelengths.items():
    # 将RGB各通道按波段权重加权
    band_img = img_array * np.array(weights).reshape(1, 1, 3)
    band_img = np.clip(band_img, 0, 255).astype(np.uint8)

    out_img = Image.fromarray(band_img)
    out_path = os.path.join(output_dir, f"apple_I_{wl}.tif")
    out_img.save(out_path)

print("生成完成！文件保存在:", output_dir)
