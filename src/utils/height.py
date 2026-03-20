import rasterio
import numpy as np
import os


def compute_height(dsm_file, dtm_file, output_file):

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with rasterio.open(dsm_file) as dsm:
        dsm_data = dsm.read(1)
        profile = dsm.profile

    with rasterio.open(dtm_file) as dtm:
        dtm_data = dtm.read(1)

    height = dsm_data - dtm_data

    with rasterio.open(output_file, "w", **profile) as dst:
        dst.write(height, 1)

    print(f"Height map saved to {output_file}")