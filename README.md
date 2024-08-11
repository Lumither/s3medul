# `s3medul`: S3 Media Uploader

`s3medul` is a python script designed for bloggers that use s3 compatible storage to serve their image/media.

## Requirements

- `ffmpeg` 

## Usage

- [] todo

## Setup

- [] todo

## Workflow

A workflow described how a media file will be processed. 

This is an example workflow for image, it automatically converts the file to .png and .webp format and upload them to remote s3 server.

```python
from core.actions import convert
from core.actions.convert import with_ffmpeg_to, to_webp
from core.actions.push_s3 import push_s3
from core.actions.register import copy, func_reg_name, append

workflow = [
    copy("main.orig_path", func_reg_name(with_ffmpeg_to, 'in')),
    convert.with_ffmpeg_to("png"),
    append(func_reg_name(with_ffmpeg_to, 'out'), func_reg_name(push_s3, 'in')),
    copy("main.orig_path", func_reg_name(to_webp, 'in')),
    convert.to_webp(),
    append(func_reg_name(to_webp, 'out'), func_reg_name(push_s3, 'in')),
    push_s3
]
```

For more details, check [the document]().

## Configuration

in the `~/.s3medul/config.json`:

```json
{
  "S3KEY": "",
  "S3SECRET": "",
  "S3BUCKET": "",
  "S3ENDPOINT": "",
  "REMOTE_ROOT_DIR": ""
}
```

Here is an example (non-working):

```json5
{
  "S3KEY": "AKIAIOSFODNN7EXAMPLE", // remote access key
  "S3SECRET": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", // remote secret key
  "S3BUCKET": "blog", // remote bucket name
  "S3ENDPOINT": "https://oss.example.com", // remote endpoint
  "REMOTE_ROOT_DIR": "/pictures" // remote root, media will be uploaded to `<S3ENDPOINT>/<S3BUCKET>/<pictures>`
}
```

## Example

```bash
python main.py -r ~/Pictures/
(1/2) /home/test_user/Pictures/Screenshots/Screenshot_20240725_161410.png
  => /tmp/s3medul/20240812015855/Screenshot_20240725_161410.png
  => /tmp/s3medul/20240812015856/Screenshot_20240725_161410.webp
  => Uploaded: https://oss.example.com/blog/pictures/Screenshot_20240725_161410.png (2.80 MiB)
  => Uploaded: https://oss.example.com/blog/pictures/Screenshot_20240725_161410.webp (390.06 KiB)            
  => Success                                                                                                  
(2/2) /home/test_user/Pictures/Anime/gothic_kiriyama_lolita.jpg
  => /tmp/s3medul/20240812015926/gothic_kiriyama_lolita.png
  => /tmp/s3medul/20240812015927/gothic_kiriyama_lolita.webp
  => Uploaded: https://oss.example.com/blog/pictures/gothic_kiriyama_lolita.png (2.50 MiB)
  => Uploaded: https://oss.example.com/blog/pictures/gothic_kiriyama_lolita.webp (563.16 KiB)                
  => Success 
```
