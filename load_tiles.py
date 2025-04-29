import sqlite3
import rasterio
import laspy
import os

def register_tiles(db_path, tif_folder, lidar_folder):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS dgm_tiles (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    left REAL, bottom REAL, right REAL, top REAL)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS lidar_tiles (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    left REAL, bottom REAL, right REAL, top REAL)""")

    # Register TIF files
    for file in os.listdir(tif_folder):
        if file.endswith('.tif'):
            path = os.path.join(tif_folder, file)
            with rasterio.open(path) as src:
                b = src.bounds
                cur.execute("INSERT INTO dgm_tiles VALUES (NULL, ?, ?, ?, ?, ?)",
                            (path, b.left, b.bottom, b.right, b.top))

    # Register LiDAR files
    for file in os.listdir(lidar_folder):
        if file.endswith('.las') or file.endswith('.laz'):
            path = os.path.join(lidar_folder, file)
            with laspy.open(path) as las:
                header = las.header
                b = header.mins[0], header.mins[1], header.maxs[0], header.maxs[1]
                cur.execute("INSERT INTO lidar_tiles VALUES (NULL, ?, ?, ?, ?, ?)",
                            (path, *b))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    register_tiles("tiles.db", "tifs", "lidar")
