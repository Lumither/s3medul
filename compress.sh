#!/bin/bash

function compress_image() {
  for png in "$@"; do
    img_name=$(basename $png ".png")
    echo "$img_name"
    pngquant --speed 1 "$png"
    if [ $? -eq 0 ]; then
      echo "Compress Successfully: $png"
    fi
  done
}

