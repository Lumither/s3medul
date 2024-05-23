#!/bin/bash

function convert_image() {
  file_list=()
  for picture in "$@"; do
    pic_name_without_ext=${picture%.*}
    ffmpeg -loglevel error -i "$picture" "${pic_name_without_ext}.png"
    if [ $? -eq 0 ]; then
      echo "Convert Successfully: ${pic_name_without_ext}.png"
      file_list+=("${pic_name_without_ext}.png")
    fi
  done
}
