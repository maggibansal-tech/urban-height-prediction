import os
import glob
import rasterio


def convert_jp2_to_tif(input_folder, output_folder):

    # create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    files = glob.glob(os.path.join(input_folder, "*.jp2"))

    print(f"Found {len(files)} JP2 files in {input_folder}")

    for f in files:

        name = os.path.basename(f).split(".")[0]
        out = os.path.join(output_folder, name + ".tif")

        # skip if already converted
        if os.path.exists(out):
            continue

        try:
            with rasterio.open(f) as src:
                profile = src.profile
                data = src.read()

            profile.update(driver="GTiff")

            with rasterio.open(out, "w", **profile) as dst:
                dst.write(data)

        except Exception as e:
            print(f"Error processing {f}: {e}")

    print(f"Conversion finished for {input_folder}")


# -------------------------
# MAIN PIPELINE
# -------------------------

def main():

    cities = {
        "manhattan": "data/raw/nyc/manhattan/rgb_jp2",
        "brooklyn": "data/raw/nyc/brooklyn/rgb_jp2"
    }

    for city, input_path in cities.items():

        output_path = f"data/interim/nyc/{city}/rgb_tif"

        convert_jp2_to_tif(input_path, output_path)


if __name__ == "__main__":
    main()