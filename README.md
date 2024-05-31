# `s3medul`: S3 Media Uploader

`s3medul` is a shell script designed for bloggers that use s3 compatible storage to serve their image/media.

It will automatically compress and upload images to the s3 storage, and print the remote address of its different
versions.

## Requirements

- `ffmpeg`: Convert any format of media to png for compatibility
- `cwebp`: Convert png image to webp format
- [`pngquant`](https://github.com/kornelski/pngquant): Compress png media
- `openssl`: Authentication
- `curl`: HTTP client

## Usage

```bash
main.sh <path to files>
```

For example:

```bash
main.sh ./test.jpg ./test.png ./test/*
```

## Configuration

in the `.env` in the dir:

```dotenv
S3KEY=xxx           # S3 Access Key
S3SECRET=xxxxx      # S3 Sccret Key
S3BUCKET=xxxxxx     # S3 Bucket Name
S3ENDPOINT=xxxxx    # S3 Server Address
```

Here is an example (non-working):

```dotenv
S3KEY=AKIAIOSFODNN7EXAMPLE
S3SECRET=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3BUCKET=blog
S3ENDPOINT=oss.example.com
```

## Example

```bash
~/Pictures/Hongkai 3rd > tree
.
└── Elysia&Eden.jpg

1 directory, 1 file
~/Pictures/Hongkai 3rd > ~/dev/s3medul/main.sh ./*
/tmp/s3medul/1717140478071754403/orig/1717140478080742716_Elysia&Eden.jpg - 3.7M
        -> https://oss.example.com/blog/pictures/orig/1717140478080742716_Elysia&Eden.jpg

/tmp/s3medul/1717140478071754403/compr/1717140478080742716_Elysia&Eden.png - 2.5M
        -> https://oss.example.com/blog/pictures/compr/1717140478080742716_Elysia&Eden.png

/tmp/s3medul/1717140478071754403/compr/1717140478080742716_Elysia&Eden.webp - 308K
        -> https://oss.example.com/blog/pictures/compr/1717140478080742716_Elysia&Eden.webp
```
