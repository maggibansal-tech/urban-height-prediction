import rasterio

path = "data/raw/netherlands/amsterdam/dsm/R_25EZ1.tif"

with rasterio.open(path) as src:
    print(src.crs)
    print(src.res)
    print(src.bounds)