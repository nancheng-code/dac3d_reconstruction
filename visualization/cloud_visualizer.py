import open3d as o3d
import numpy as np

class CloudVisualizer:
    """
    点云可视化模块
    - 可彩色编码 z 高度
    """

    @staticmethod
    def colorize_pointcloud_by_height(pcd):
        points = np.asarray(pcd.points)
        z = points[:, 2]
        z_norm = (z - z.min()) / (z.max() - z.min() + 1e-8)

        colors = np.zeros_like(points)
        colors[:, 0] = z_norm
        colors[:, 1] = 1 - z_norm / 2
        colors[:, 2] = 1 - z_norm

        pcd.colors = o3d.utility.Vector3dVector(colors)
        return pcd

    @staticmethod
    def visualize(pcd, window_name="PointCloud", point_size=2.0, background_color=(0.1, 0.1, 0.1)):
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name=window_name, width=800, height=600)
        vis.add_geometry(pcd)
        vis.get_render_option().background_color = np.array(background_color)
        vis.get_render_option().point_size = point_size
        vis.get_render_option().show_coordinate_frame = True
        vis.run()
        vis.destroy_window()

    @staticmethod
    def from_ply(file_path):
        pcd = o3d.io.read_point_cloud(file_path)
        return pcd


if __name__ == "__main__":
    import os
    from reconstruction.cloud_filter import CloudFilter
    from reconstruction.height_calculator import HeightCalculator
    from preprocessing.preprocessing_pipeline import run_preprocessing

    # 1️ 预处理图像
    img = run_preprocessing()

    # 2️ 高度图
    lut_path = os.path.join(os.path.dirname(__file__), "..", "reconstruction", "apple_lut.npy")
    hc = HeightCalculator(lut_path)
    height_map = hc.compute_height_map(img)

    # 3️ 高度图 → 点云
    cf = CloudFilter()
    pcd = cf.heightmap_to_pointcloud(height_map)

    # 4️ 滤波
    pcd_filtered = cf.statistical_filter(pcd, nb_neighbors=20, std_ratio=2.0)

    # 5️ 彩色编码
    pcd_colored = CloudVisualizer.colorize_pointcloud_by_height(pcd_filtered)

    # 6️ 可视化
    CloudVisualizer.visualize(pcd_colored, window_name="Apple PointCloud", point_size=2.0)
