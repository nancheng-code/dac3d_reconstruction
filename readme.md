# 🍎 DAC-3D 苹果三维重建项目

本项目基于**多波长共聚焦成像（DAC-3D）**技术，实现了苹果样品的三维高度图重建与点云可视化。项目涵盖了从图像预处理到最终可视化的完整流程。

---

## 📁 项目结构

项目采用模块化设计，结构清晰，便于维护和扩展。

```bash
dac3d_reconstruction/
│
├─ data/                      # 数据存储目录
│ ├─ raw/                    # 原始多波长图像（如 apple.jpg 或 TIFF）
│ └─ processed/              # 处理后的图像、高度图、点云等
│
├─ preprocessing/             # 图像预处理模块
│ ├─ image_loader.py         # 读取默认样品图像
│ ├─ background_correction.py# 暗场校正
│ ├─ image_registration.py   # 多通道图像配准
│ ├─ gaussian_filter.py      # 高斯滤波去噪
│ └─ preprocessing_pipeline.py# 整体预处理流程
│
├─ reconstruction/            # 重建核心模块
│ ├─ simulate_lut.py         # 生成模拟 LUT
│ ├─ height_calculator.py    # 高度图计算
│ └─ cloud_filter.py         # 点云滤波和保存
│
├─ visualization/            # 可视化脚本
│ └─ visualize.py            # 高度图/点云可视化
│
└─ test/                     # 测试与运行入口
    └─ run.py                # 完整运行示例

🚀 快速开始
1. 环境准备
建议使用 Conda 管理环境，以确保依赖兼容。
# 1. 创建新的 Conda 环境 (Python 3.10)
conda create -n open3d python=3.10
conda activate open3d

# 2. 安装依赖
# 在项目根目录下执行
pip install -r requirements.txt

2. 运行项目
在项目根目录下执行以下命令，即可启动完整流程：
python -m test.run
执行流程：
图像预处理（暗场校正 + 配准 + 高斯滤波）
模拟 LUT 生成
高度图计算
点云生成与滤波
可视化展示
输出结果：
高度图： data/processed/apple_height_map.tif
点云文件： data/processed/apple_pointcloud.ply

🛠️ 自定义其他物品建模
如果你想使用其他物品的图片进行建模，请按以下步骤修改：
上传图片： 将你的图片上传至项目目录。
修改路径： 在 generate_data.py (或相关脚本) 中，更改输入路径：
input_path = "your_custom_image.jpg"  # 替换为你上传的图片路径
更新 LUT： 在 LUT.py (或 simulate_lut.py) 中，更新为你上传图片对应的 LUT 仿真表（需自行根据光学特性合理计算）。

📊 结果展示
以下是项目的重建效果示例：
表格
原图	3D 重建效果
图 1 & 2： 苹果原图与生成的 3D 高度图示例。
💡 特别说明
这是本人第一次上传的实验小项目，代码和算法仍有优化空间。
版本兼容性： 请特别注意 requirements.txt 中库的版本，特别是 Open3D 和 OpenCV 的兼容性。
欢迎反馈： 如有不足之处，欢迎提出建议和改进意见，共同完善该项目！
