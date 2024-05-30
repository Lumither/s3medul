#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. "$DIR/.env"
. "$DIR/.env.local"

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
mkdir -p "$tmp_work_dir/cmprs"
cmprs_pics=()
for pic in "${cvt_pics[@]}"; do
  raw_pic_name="$(basename "$pic")"
  new_png_path="${tmp_work_dir}/cmprs/${raw_pic_name}"
  new_webp_path="${new_png_path%.*}.webp"
  pngquant --speed 1 "$pic" --output "$new_png_path"
  if [ $? -eq 0 ]; then
    cmprs_pics+=("$new_png_path")
  fi
  cwebp "$pic" -o "$new_webp_path" -quiet
  if [ $? -eq 0 ]; then
    cmprs_pics+=("$new_webp_path")
  fi
done

# push file to s3 storage
for pic in "${cmprs_pics[@]}"; do
  remote_addr="$S3ENDPOINT"
  resource="/${S3BUCKET}/pictures/$(basename "$pic")"
  content_type="application/octet-stream"
  date=$(date -R)
  _signature="PUT\n\n${content_type}\n${date}\n${resource}"
  signature=$(echo -en "${_signature}" | openssl sha1 -hmac "${S3SECRET}" -binary | base64)
  curl -X PUT -T "${pic}" \
       -H "Host: ${S3ENDPOINT}" \
       -H "Date: ${date}" \
       -H "Content-Type: ${content_type}" \
       -H "Authorization: AWS ${S3KEY}:${signature}" \
       "https://${remote_addr}${resource}"
done

#res=$(convert_image "$@")
#echo "$res"
#compress_image "$1"
