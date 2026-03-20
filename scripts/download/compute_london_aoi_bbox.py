from pyproj import Transformer

# WGS84 (lat/lon)
min_lon, max_lon = -0.15, -0.05
min_lat, max_lat = 51.48, 51.54

# Convert WGS84 -> British National Grid (EPSG:27700)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)

min_x, min_y = transformer.transform(min_lon, min_lat)
max_x, max_y = transformer.transform(max_lon, max_lat)

print("EPSG:27700 Bounding Box:")
print(f"Min X: {min_x}")
print(f"Max X: {max_x}")
print(f"Min Y: {min_y}")
print(f"Max Y: {max_y}")