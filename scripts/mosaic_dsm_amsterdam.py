from src.utils.mosaic import mosaic_rasters

#creating mosaic of the dsm rasters for amsterdam
mosaic_rasters(
    "data/raw/netherlands/amsterdam/dsm",
    "data/interim/netherlands/amsterdam/amsterdam_dsm.tif"
)