import rasterio
import numpy as np
import matplotlib.pyplot as plt

rgb_path = "data/interim/netherlands/amsterdam/amsterdam_rgb.tif"
height_path = "data/processed/netherlands/amsterdam_height.tif"

# -----------------------------
# Load RGB
# -----------------------------
with rasterio.open(rgb_path) as src:
    rgb = src.read([1,2,3])
    rgb = np.transpose(rgb, (1,2,0))

# normalize RGB
rgb = rgb.astype(np.float32)
rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())

# -----------------------------
# Load height
# -----------------------------
with rasterio.open(height_path) as src:
    height = src.read(1)

# clip extreme heights for visualization
height = np.clip(height, 0, 80)

# normalize height
height_norm = (height - height.min()) / (height.max() - height.min())

# -----------------------------
# Plot figure
# -----------------------------
fig, ax = plt.subplots(1,3, figsize=(18,6))

# RGB
ax[0].imshow(rgb)
ax[0].set_title("RGB Orthophoto")
ax[0].axis("off")

# height map
h = ax[1].imshow(height, cmap="viridis")
ax[1].set_title("Building Height Map (DSM − DTM)")
ax[1].axis("off")
plt.colorbar(h, ax=ax[1], fraction=0.046, pad=0.04)

# overlay
ax[2].imshow(rgb)
ax[2].imshow(height_norm, cmap="inferno", alpha=0.45)
ax[2].set_title("RGB + Height Overlay")
ax[2].axis("off")

plt.tight_layout()
plt.show()