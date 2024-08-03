#!/bin/bash

# push file to s3 storage
function s3upload() {
  local file="$1"
  local filepath="$2"

  local S3ENDPOINT="$3"
  local S3BUCKET="$4"
  local S3KEY="$5"
  local S3SECRET="$6"

  local content_type="$7"

  local resource="/${S3BUCKET}/${filepath}"
  local date=$(date -R)
  local _signature="PUT\n\n${content_type}\n${date}\n${resource}"
  local signature=$(echo -en "${_signature}" | openssl sha1 -hmac "${S3SECRET}" -binary | base64)
  curl \
    -X PUT -T "${file}" \
    -H "Host: ${S3ENDPOINT}" \
    -H "Date: ${date}" \
    -H "Content-Type: ${content_type}" \
    -H "Authorization: AWS ${S3KEY}:${signature}" \
    "https://${S3ENDPOINT}${resource}" \
    --retry 5 --retry-all-errors
  printf "%s - %s\n\t-> https://%s%s\n\n" "${file}" "$(du -sh "$file" | sed 's/\s.*//')" "${S3ENDPOINT}" "${resource}"
}
