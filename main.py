import json
import os.path
import sys

import pandas as pd

import cli
from core.ansi import Ansi
from core.s3 import S3
from core.workflow import *

workflow = [set_mime, set_workflow]


def search_path(directory):
    return [str(file) for file in Path(directory).rglob('*') if file.is_file()]


def main():
    args = cli.parse_args()

    config_path = os.path.abspath(os.path.expanduser(args.config))
    config_file = open(config_path, 'r')
    config = json.load(config_file)
    s3cli: S3 = S3(
        access_key=config['S3KEY'],
        secret_key=config['S3SECRET'],
        bucket_name=config['S3BUCKET'],
        endpoint=config['S3ENDPOINT'],
    )

    work_files = []
    if args.recursive:
        work_files = search_path(args.path)
    else:
        if Path(args.path).is_dir():
            print("Error: use `-r` flag for directory", file=sys.stderr)
        else:
            work_files.append(args.path)

    mime_db = pd.read_csv(args.database)

    cnt = 1
    for f_path in work_files:
        print(f"({cnt}/{len(work_files)}) {Ansi.blend(Ansi.BOLD, f_path)}")
        try:
            wf_msg = {
                "wf_orig_path": f_path,
                "wf_work_path": f_path,
                "wf_compress": args.compress,
                "wf_cprs_path": [],
                "wf_upload_queue": [f_path],
                "wf_remote_root_dir": config["REMOTE_ROOT_DIR"],
                "wf_mime_db": mime_db,
                "wf_s3instance": s3cli
            }
            for func in workflow:
                wf_msg = func(wf_msg)
            print(Ansi.blend(Ansi.GREEN, f"  => Success"))
        except Exception as e:
            print(Ansi.blend(Ansi.RED, f"  => Error: {str(e)}"), file=sys.stderr)

        cnt += 1


if __name__ == '__main__':
    main()
