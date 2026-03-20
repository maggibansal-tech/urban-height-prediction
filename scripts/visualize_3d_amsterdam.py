import rasterio
import numpy as np
import pyvista as pv

# -----------------------------------
# FILE PATHS
# -----------------------------------
rgb_path = "data/interim/netherlands/amsterdam/amsterdam_rgb.tif"
height_path = "data/processed/netherlands/amsterdam_height.tif"

# -----------------------------------
# LOAD HEIGHT
# -----------------------------------
with rasterio.open(height_path) as src:
    height = src.read(1)

# downsample for visualization
ds = 4
height = height[::ds, ::ds]

height = np.clip(height, 0, 120)

h, w = height.shape

# -----------------------------------
# LOAD RGB
# -----------------------------------
with rasterio.open(rgb_path) as src:
    rgb = src.read([1,2,3])

rgb = np.transpose(rgb, (1,2,0))
rgb = rgb[::ds, ::ds]

rgb = rgb.astype(np.uint8)

# -----------------------------------
# CREATE GRID
# -----------------------------------
x = np.arange(w)
y = np.arange(h)

X, Y = np.meshgrid(x, y)

grid = pv.StructuredGrid(X, Y, height)

# height exaggeration
grid.points[:, 2] *= 2

# -----------------------------------
# CREATE TEXTURE COORDINATES
# -----------------------------------
u = np.linspace(0, 1, w)
v = np.linspace(0, 1, h)

U, V = np.meshgrid(u, v)

texture_coords = np.c_[U.ravel(), V.ravel()]
grid.active_texture_coordinates = texture_coords

# -----------------------------------
# CREATE TEXTURE
# -----------------------------------
texture = pv.numpy_to_texture(rgb)

# -----------------------------------
# PLOT
# -----------------------------------
plotter = pv.Plotter(window_size=(1600,900))

plotter.add_mesh(
    grid,
    texture=texture,
    smooth_shading=True
)

plotter.add_axes()

plotter.camera_position = 'iso'

plotter.show()