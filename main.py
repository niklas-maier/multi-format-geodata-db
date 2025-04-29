from query import DGMDatabase

db = DGMDatabase("tiles.db")

lat = 47.697545
lon = 9.061124

print("Height:", db.get_height(lat, lon))

#points = db.get_lidar_points(lat, lon)
print("Found", len(points), "LiDAR points nearby")

db.close()

# To-DO 
# ignore empty input folders
# query grid point cloud