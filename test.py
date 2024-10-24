import json
import time
from pathlib import Path

import boto3
import rasterio
from rio_tiler.io.rasterio import Reader

S3_BUCKET = "kitware-nitf-cog-comparison-test"

# Initialize S3 client
s3 = boto3.client("s3")


def chip_image(
    img_name: str,
    img_url: str,
    bbox: tuple[float, float, float, float],
    output_dir: Path,
):
    with rasterio.Env(
        GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
        GDAL_HTTP_MERGE_CONSECUTIVE_RANGES="YES",
        GDAL_HTTP_MULTIPLEX="YES",
        GDAL_HTTP_VERSION=2,
    ):
        with Reader(input=img_url) as img:
            img_chip = img.part(bbox=bbox)
            print(img_chip.height, img_chip.width)


def main():
    output_dir = Path(__file__).parent / "chips"
    output_dir.mkdir(exist_ok=True)
    results_dest = Path(__file__).parent / "results.json"
    results = {}

    bboxes = json.loads((Path(__file__).parent / "bounding_boxes.json").read_text())

    for filename, bbox in bboxes.items():
        base_url = f"s3://{S3_BUCKET}/"
        nitf_url = base_url + filename + ".nitf"
        tif_url = base_url + "converted_cogs/" + filename + ".nitf.tif"
        bbox = bbox["x_min"], bbox["y_min"], bbox["x_max"], bbox["y_max"]
        nitf_filesize = (Path(__file__).parent / f"{filename}.nitf").stat().st_size

        print(filename)
        print(f"\tNitf file size: {nitf_filesize / 1024 / 1024} MB")

        print(f"\tChipping {filename} COG")
        start_time = time.monotonic()
        chip_image(filename, tif_url, bbox, output_dir)
        cog_time = time.monotonic() - start_time
        print(f"\tDone chipping {filename} COG in {cog_time} seconds")

        print(f"\tChipping {filename} NITF")
        start_time = time.monotonic()
        chip_image(filename, nitf_url, bbox, output_dir)
        nitf_time = time.monotonic() - start_time
        print(f"\tDone chipping {filename} NITF in {nitf_time} seconds")
        print()

        results[filename] = {
            "cog_time": cog_time,
            "nitf_time": nitf_time,
            "nitf_filesize": nitf_filesize,
        }

    results_dest.write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
