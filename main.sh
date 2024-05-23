#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. "$DIR/compress.sh"
. "$DIR/convert.sh"

convert_image "$@"
#compress_image "$1"
