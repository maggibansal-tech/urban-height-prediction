import os
import requests
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import box
import geopandas as gpd

# ==============================
# CONFIG
# ==============================

OUTPUT_DIR = "raw_data/nyc"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Official NYC datasets (stable government endpoints)

# NYC 2018 Orthophoto (Manhattan GeoTIFF)
NYC_ORTHO_URL = "https://s3.amazonaws.com/nyc-orthoimagery/2018/manhattan.tif"

# NYC 2017 DEM raster
NYC_DEM_URL = "https://s3.amazonaws.com/nyc-dem/DEM_2017_1m.tif"

# AOIs (WGS84)
AOIS = {
    "manhattan_block": (-74.005, 40.745, -73.975, 40.765),
    "brooklyn_block": (-73.965, 40.710, -73.930, 40.735),
}

TARGET_CRS = "EPSG:32618"  # UTM Zone 18N (NYC)
TARGET_RES = 0.5  # meters


# ==============================
# DOWNLOAD FUNCTION
# ==============================

def download_file(url, output_path):
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        return

    print(f"Downloading {url}")
    r = requests.get(url, stream=True)
    r.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Saved to {output_path}")


# ==============================
# CLIP RASTER
# ==============================

def clip_raster(input_path, bbox, output_path):
    geom = box(*bbox)
    gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")

    with rasterio.open(input_path) as src:
        gdf = gdf.to_crs(src.crs)

        clipped, transform = mask(src, gdf.geometry, crop=True)

        meta = src.meta.copy()
        meta.update({
            "height": clipped.shape[1],
            "width": clipped.shape[2],
            "transform": transform
        })

        with rasterio.open(output_path, "w", **meta) as dst:
            dst.write(clipped)

    print(f"Clipped raster saved: {output_path}")


# ==============================
# REPROJECT + RESAMPLE
# ==============================

def reproject_resample(input_path, output_path):

    with rasterio.open(input_path) as src:

        transform, width, height = calculate_default_transform(
            src.crs,
            TARGET_CRS,
            src.width,
            src.height,
            *src.bounds,
            resolution=TARGET_RES
        )

        kwargs = src.meta.copy()
        kwargs.update({
            "crs": TARGET_CRS,
            "transform": transform,
            "width": width,
            "height": height
        })

        with rasterio.open(output_path, "w", **kwargs) as dst:

            for i in range(1, src.count + 1):

                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=TARGET_CRS,
                    resampling=Resampling.bilinear
                )

    print(f"Reprojected and resampled: {output_path}")


# ==============================
# MAIN WORKFLOW
# ==============================

if __name__ == "__main__":

    ortho_full = os.path.join(OUTPUT_DIR, "nyc_ortho_full.tif")
    dem_full = os.path.join(OUTPUT_DIR, "nyc_dem_full.tif")

    # Step 1 — Download datasets
    download_file(NYC_ORTHO_URL, ortho_full)
    download_file(NYC_DEM_URL, dem_full)

    # Step 2 — Process AOIs
    for name, bbox in AOIS.items():

        ortho_clip = os.path.join(OUTPUT_DIR, f"{name}_ortho_clip.tif")
        dem_clip = os.path.join(OUTPUT_DIR, f"{name}_dem_clip.tif")

        clip_raster(ortho_full, bbox, ortho_clip)
        clip_raster(dem_full, bbox, dem_clip)

        ortho_final = os.path.join(OUTPUT_DIR, f"{name}_ortho_0p5m.tif")
        dem_final = os.path.join(OUTPUT_DIR, f"{name}_dem_0p5m.tif")

        reproject_resample(ortho_clip, ortho_final)
        reproject_resample(dem_clip, dem_final)

    print("\nNYC blocks prepared successfully.")