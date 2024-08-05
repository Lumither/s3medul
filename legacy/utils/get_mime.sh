#!/bin/bash


function get_mime() {
  local DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local CSV_PATH="$DIR/../mime.csv"
  local res="$(csvsql --query "select typ from mime where ext = \"$1\";" "$CSV_PATH")"
  echo -e "$res" | tail -n 1
}
