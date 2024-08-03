#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$DIR/.env"
source "$DIR/.env.local"

source "$DIR/utils/get_mime.sh"
source "$DIR/utils/s3upload.sh"

# copy to tmp workplace
tmp_work_dir="/tmp/s3medul/$(date +%s%N)"
mkdir -p "$tmp_work_dir"
mkdir -p "$tmp_work_dir/orig"
orig_pics=()
for pic in "$@"; do
  tmp_pic="${tmp_work_dir}/orig/$(date +%s%N)_$(basename "$pic")"
  cp "$pic" "$tmp_pic"
  orig_pics+=("$tmp_pic")
done

# convert to png
mkdir -p "$tmp_work_dir/cvt"
cvt_pics=()
for pic in "${orig_pics[@]}"; do
  raw_pic_name="$(basename "$pic")"
  new_pic_name="${raw_pic_name%.*}.png"
  new_pic_path="${tmp_work_dir}/cvt/${new_pic_name}"
  ffmpeg -loglevel error -i "$pic" "${new_pic_path}"
  if [ $? -eq 0 ]; then
    cvt_pics+=("$new_pic_path")
  fi
done

# compress img
mkdir -p "$tmp_work_dir/compr"
compr_pics=()
for pic in "${cvt_pics[@]}"; do
  raw_pic_name="$(basename "$pic")"
  new_png_path="${tmp_work_dir}/compr/${raw_pic_name}"
  new_webp_path="${new_png_path%.*}.webp"
#  pngquant --speed 1 "$pic" --output "$new_png_path"
#  if [ $? -eq 0 ]; then
#    compr_pics+=("$new_png_path")
#  fi
  cwebp "$pic" -o "$new_webp_path" -quiet
  if [ $? -eq 0 ]; then
    compr_pics+=("$new_webp_path")
  fi
done

# push orig img
for pic in "${orig_pics[@]}"; do
  f_name=$(basename "$pic")
  f_ext="${f_name##*.}"
  mime="$(get_mime "$f_ext")"
  s3upload "$pic" "pictures/orig/${f_name}" "$S3ENDPOINT" "$S3BUCKET" "$S3KEY" "$S3SECRET" "$mime"
done
# push compressed img
for pic in "${compr_pics[@]}"; do
  f_name=$(basename "$pic")
  f_ext="${f_name##*.}"
  mime="$(get_mime "$f_ext")"
  s3upload "$pic" "pictures/compr/${f_name}" "$S3ENDPOINT" "$S3BUCKET" "$S3KEY" "$S3SECRET" "$mime"
done
