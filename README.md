# Lidar & DGM Query Project

> ⚠️ **Work in Progress**  
> This project is currently under development and not ready for production use. Features, usage, and structure may change.

This project allows querying DGM height data from GeoTIFF and nearby LiDAR points from LAS/LAZ files.

## Usage

1. Put your `.tif` files into `/tifs/`
2. Put your LIDAR files into `/lidar/`
3. Run `load_tiles.py` to build the database
4. Use `main.py` to test queries
