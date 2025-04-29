import sqlite3
import rasterio
import laspy
import numpy as np
from scipy.spatial import KDTree
from utils.geo_utils import wgs84_to_utm32

class DGMDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def get_height(self, lat, lon):
        x, y = wgs84_to_utm32(lon, lat)

        res = self.cur.execute("""
            SELECT filename FROM dgm_tiles
            WHERE left <= ? AND right >= ? AND bottom <= ? AND top >= ?
        """, (x, x, y, y)).fetchone()

        if not res:
            raise ValueError("No DGM tile found.")

        with rasterio.open(res[0]) as src:
            row, col = src.index(x, y)
            return src.read(1)[row, col]

    def get_lidar_points(self, lat, lon, radius=2):
        x, y = wgs84_to_utm32(lon, lat)

        res = self.cur.execute("""
            SELECT filename FROM lidar_tiles
            WHERE left <= ? AND right >= ? AND bottom <= ? AND top >= ?
        """, (x, x, y, y)).fetchone()

        if not res:
            raise ValueError("No LiDAR tile found.")

        with laspy.open(res[0]) as las:
            points = las.read().points
            coords = np.vstack((points.x, points.y)).T
            tree = KDTree(coords)
            idx = tree.query_ball_point([x, y], radius)
            return points[idx]

    def close(self):
        self.conn.close()
