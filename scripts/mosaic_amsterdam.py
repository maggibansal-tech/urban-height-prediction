from src.utils.mosaic import mosaic_rasters

#First: Amsterdam
# 1.1 Mosaic for dsm of amsterdam
mosaic_rasters(
    "data/raw/netherlands/amsterdam/dsm",
    "data/interim/netherlands/amsterdam/amsterdam_dsm.tif"
)
#1.2 Mosaic for dtm of amsterdam
mosaic_rasters(
    "data/raw/netherlands/amsterdam/dtm",
    "data/interim/netherlands/amsterdam/amsterdam_dtm.tif"
)
#1.3 Mosaic for RGB of amsterdam
mosaic_rasters(
    "data/raw/netherlands/amsterdam/rgb",
    "data/interim/netherlands/amsterdam/amsterdam_rgb.tif"
)
#Second: Rotterdam
# 2.1 Mosaic for dsm of rotterdam
mosaic_rasters(
    "data/raw/netherlands/rotterdam/dsm",
    "data/interim/netherlands/rotterdam/rotterdam_dsm.tif"
)
# 2.2 Mosaic for dtm of rotterdam
mosaic_rasters(
    "data/raw/netherlands/rotterdam/dtm",
    "data/interim/netherlands/rotterdam/rotterdam_dtm.tif"
)
# 2.3 Mosaic for RGB of rotterdam
mosaic_rasters(
    "data/raw/netherlands/rotterdam/rgb",
    "data/interim/netherlands/rotterdam/rotterdam_rgb.tif"
)