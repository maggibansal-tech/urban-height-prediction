import glob
import os
import rasterio
from rasterio.merge import merge


def mosaic_rasters(input_folder, output_file):

    # create output directory automatically
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    files = glob.glob(f"{input_folder}/*.tif")

    if len(files) == 0:
        raise ValueError(f"No raster files found in {input_folder}")

    print(f"Found {len(files)} tiles")

    srcs = [rasterio.open(f) for f in files]

    mosaic, transform = merge(srcs)

    profile = srcs[0].profile
    profile.update(
        height=mosaic.shape[1],
        width=mosaic.shape[2],
        transform=transform,
        count=mosaic.shape[0]   # important for RGB
    )

    with rasterio.open(output_file, "w", **profile) as dst:
        dst.write(mosaic)

    print(f"Mosaic saved to {output_file}")