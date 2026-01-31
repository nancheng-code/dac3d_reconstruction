import numpy as np
import open3d as o3d
import os


class CloudFilter:
    """
    点云滤波模块
    """

    @staticmethod
    def heightmap_to_pointcloud(height_map, scale_xy=1.0):
        H, W = height_map.shape
        xx, yy = np.meshgrid(np.arange(W), np.arange(H))
        mask = ~np.isnan(height_map)

        x = xx[mask] * scale_xy
        y = yy[mask] * scale_xy
        z = height_map[mask]

        points = np.stack([x, y, z], axis=1)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        return pcd

    @staticmethod
    def statistical_filter(pcd, nb_neighbors=20, std_ratio=2.0):
        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors,
                                                 std_ratio=std_ratio)
        filtered_pcd = pcd.select_by_index(ind)
        return filtered_pcd

    @staticmethod
    def radius_filter(pcd, radius=0.5, min_neighbors=5):
        cl, ind = pcd.remove_radius_outlier(nb_points=min_neighbors,
                                            radius=radius)
        filtered_pcd = pcd.select_by_index(ind)
        return filtered_pcd

    @staticmethod
    def save_pointcloud(pcd, filename="pointcloud.ply"):
        out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, filename)
        o3d.io.write_point_cloud(path, pcd)
        print(f"点云已保存: {path}")
        return path
