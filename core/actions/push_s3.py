import os
from pathlib import Path

from core.actions.register import get_reg
from core.ansi import Ansi
from core.s3 import S3
from core.utils import sizeof_fmt, ensure_list, get_file_mime


def push_s3(wf_msg):
    for file in ensure_list(get_reg(wf_msg, push_s3, 'in')):
        s3instance: S3 = wf_msg['wf_s3instance']
        basename = os.path.basename(file)
        remote_path = f"{''.join(wf_msg['wf_remote_root_dir'].split('/'))}/{basename}"
        remote_url = f"{s3instance.endpoint}/{s3instance.bucket_name}/{remote_path}"
        file_size = Path(file).stat().st_size
        print(f"  => {remote_url}", end='', flush=True)
        s3instance.upload_file(file, remote_path, get_file_mime(wf_msg['wf_mime_db'], file))
        print(Ansi.blend(Ansi.GREEN, f"\r  => Uploaded: {remote_url} ({sizeof_fmt(file_size)})"))


