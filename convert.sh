#!/bin/bash

# Directory to iterate over
directory=$(pwd)

# Loop through each file in the directory
for file in "$directory"/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Processing file: $filename"
        gdal_translate "$filename" "converted_cogs/$filename.tif" -of COG \
          -co TILING_SCHEME=GoogleMapsCompatible \
          -co COMPRESS=LZW \
          -co BLOCKSIZE=512 \
          -co OVERVIEW_RESAMPLING=NEAREST \
          -co COPY_SRC_OVERVIEWS=YES
    fi
done
