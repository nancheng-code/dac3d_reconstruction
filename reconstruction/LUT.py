import numpy as np
import os


def simulate_apple_lut(delta_range1=(-50, 50), delta_range2=(-50, 50), num_points=200):
    """
    模拟苹果三波长 DAC 系统的 LUT
    delta1: I_525 - I_460
    delta2: I_620 - I_525
    输出 z 高度值
    """
    delta1_vals = np.linspace(delta_range1[0], delta_range1[1], num_points)
    delta2_vals = np.linspace(delta_range2[0], delta_range2[1], num_points)

    # 构建 2D 网格
    D1, D2 = np.meshgrid(delta1_vals, delta2_vals, indexing='ij')

    # 模拟高度关系，可以用任意连续函数
    # 这里使用简单函数：z = a*delta1 + b*delta2 + c*sin(delta1/10)*cos(delta2/10)
    a, b, c = 0.1, 0.15, 5.0  # 调整系数
    Z = a * D1 + b * D2 + c * np.sin(D1 / 10) * np.cos(D2 / 10)

    # 输出 LUT: 字典形式
    lut = {
        'delta1': delta1_vals,
        'delta2': delta2_vals,
        'z': Z
    }
    return lut

def save_lut(lut, filename="apple_lut.npy"):
    out_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    np.save(path, lut)
    print(f"✅ 模拟 LUT 已保存: {path}")
    return path


if __name__ == "__main__":
    lut = simulate_apple_lut()
    save_lut(lut)
