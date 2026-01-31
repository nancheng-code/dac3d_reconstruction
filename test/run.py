import os
import numpy as np
from preprocessing.preprocessing_pipeline import run_preprocessing
from reconstruction.height_calculator import HeightCalculator
from reconstruction.cloud_filter import CloudFilter
import open3d as o3d
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib import rcParams


# -------------------------------
# 1️ 图像预处理
# -------------------------------
print("开始图像预处理...")
img = run_preprocessing()
print("预处理完成。图像形状:", img.shape)

# -------------------------------
# 2️ 模拟 LUT 并生成高度图
# -------------------------------
lut_path = os.path.join(os.path.dirname(__file__), "..", "reconstruction", "apple_lut.npy")
print("开始生成高度图...")
hc = HeightCalculator(lut_path)
height_map = hc.compute_height_map(img)
print("高度图生成完成")
print("高度图 NaN 占比:", np.sum(np.isnan(height_map))/height_map.size * 100, "%")

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 黑体
rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# height_map绘制
plt.imshow(height_map, cmap='jet')
plt.colorbar()
plt.title("高度图", fontsize=16)
plt.xlabel("X轴")
plt.ylabel("Y轴")
plt.show()

#  构建点云
print("开始生成点云...")
pcd = CloudFilter.heightmap_to_pointcloud(height_map)

# 点云滤波
pcd_filtered = CloudFilter.statistical_filter(pcd)
print("滤波后点云数量:", len(np.asarray(pcd_filtered.points)))

# 可视化
o3d.visualization.draw_geometries([pcd_filtered], window_name="Apple Point Cloud")

# 6 保存
CloudFilter.save_pointcloud(pcd_filtered, "apple_pointcloud.ply")