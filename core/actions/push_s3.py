import os
from pathlib import Path

from core.ansi import Ansi
from core.s3 import S3
from core.utils import sizeof_fmt


def push_s3(wf_msg):
    for file in wf_msg['wf_upload_queue']:
        s3instance: S3 = wf_msg['wf_s3instance']
        basename = os.path.basename(file)
        remote_path = f"{wf_msg['wf_remote_root_dir']}/{basename}"
        remote_url = f"{s3instance.endpoint}/{s3instance.bucket_name}/{remote_path}"
        file_size = Path(file).stat().st_size
        print(f"  => {remote_url}", end='', flush=True)
        s3instance.upload_file(file, remote_path, wf_msg["wf_mime"])
        print(Ansi.blend(Ansi.GREEN, f"\r  => {remote_url} ({sizeof_fmt(file_size)})"))

