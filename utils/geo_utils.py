from pyproj import Transformer

# Transformer for WGS84 -> UTM32N (EPSG:25832)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:25832", always_xy=True)

def wgs84_to_utm32(lon, lat):
    """Convert WGS84 lat/lon to UTM32 coordinates"""
    x, y = transformer.transform(lon, lat)
    return x, y

