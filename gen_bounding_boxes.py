import json
import random
from pathlib import Path

import boto3
from rasterio.transform import xy
from rio_tiler.io import Reader

# Initialize S3 client
s3 = boto3.client("s3")


def download_nitf_files(path: Path):
    """Download all .NITF files from the S3 bucket to the local directory."""
    bucket_name = "kitware-nitf-cog-comparison-test"
    response = s3.list_objects_v2(Bucket=bucket_name)
    nitf_files: list[str] = [
        obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".nitf")
    ]
    for nitf_file in nitf_files:
        dest = path / nitf_file
        if dest.exists():
            print(f"Skipping '{nitf_file}' download because it already exists.")
            continue
        print(f"Downloading {nitf_file} to {dest}")
        s3.download_file(bucket_name, nitf_file, str(dest))


def generate_random_bbox_geospatial(transform, width, height):
    """Generate a random bounding box in geospatial (EPSG:4326) coordinates."""
    # Generate random pixel coordinates within image bounds
    factor = 4
    x_min_px = random.randint(0, width // factor)
    y_min_px = random.randint(0, height // factor)
    x_max_px = x_min_px + width // factor
    y_max_px = y_min_px + height // factor

    # Convert pixel coordinates to geospatial coordinates (EPSG:4326)
    top_left = xy(transform, y_min_px, x_min_px, offset="ul")
    bottom_right = xy(transform, y_max_px, x_max_px, offset="lr")

    # Bounding box in geospatial coordinates (lon/lat)
    bbox = {
        "x_min": top_left[0],  # longitude min
        "y_min": bottom_right[1],  # latitude min
        "x_max": bottom_right[0],  # longitude max
        "y_max": top_left[1],  # latitude max
    }
    return bbox


def main():
    nitf_dir = Path(__file__).parent
    bboxes = {}
    bbox_json = Path(__file__).parent / "bounding_boxes.json"

    download_nitf_files(nitf_dir)

    for nitf in nitf_dir.glob("*.nitf"):
        print("Generating bounding boxes for", nitf.stem)

        with Reader(nitf) as cog:
            # Get image dimensions and transform
            img_info = cog.info()
            width = img_info.width
            height = img_info.height
            transform = cog.dataset.transform  # Affine transform of the image

            # Generate a random bounding box in geospatial coordinates (EPSG:4326)
            bbox = generate_random_bbox_geospatial(transform, width, height)

            # Save bounding box to JSON
            bboxes[nitf.stem] = bbox

    # Write the bounding boxes to a JSON file
    bbox_json.write_text(json.dumps(bboxes, indent=2))
    print(f"Bounding boxes saved to {bbox_json}")


if __name__ == "__main__":
    main()
