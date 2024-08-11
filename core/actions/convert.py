import tempfile
from datetime import datetime
from pathlib import Path

from PIL import Image

import ffmpeg

from core.actions.register import get_reg
from core.ansi import Ansi
from core.utils import ensure_list


def with_ffmpeg_to(to_format: str, prefix: str = '', suffix: str = ''):
    def func(wf_msg):
        res_list: list = get_reg(wf_msg, with_ffmpeg_to, 'out', [])
        work_path = f"{tempfile.gettempdir()}/s3medul/{datetime.now().strftime("%Y%m%d%H%M%S")}"
        Path(work_path).mkdir(parents=True, exist_ok=True)
        for file in ensure_list(get_reg(wf_msg, with_ffmpeg_to, 'in')):
            basename_without_ext = Path(file).with_suffix("").resolve().name
            new_name = f"{prefix}{basename_without_ext}{suffix}.{to_format}"
            new_path = f"{work_path}/{new_name}"
            (
                ffmpeg
                .input(file)
                .output(new_path)
                .run(quiet=True)
            )
            res_list.append(new_path)
            print(Ansi.blend(Ansi.GREEN,
                             f"  => {new_path}"
                             ))
        return wf_msg

    return func


def to_webp(prefix: str = '', suffix: str = '', quality=100):
    def func(wf_msg):
        res_list: list = get_reg(wf_msg, to_webp, 'out', [])
        work_path = f"{tempfile.gettempdir()}/s3medul/{datetime.now().strftime("%Y%m%d%H%M%S")}"
        Path(work_path).mkdir(parents=True, exist_ok=True)
        for file in ensure_list(get_reg(wf_msg, to_webp, 'in')):
            basename_without_ext = Path(file).with_suffix("").resolve().name
            new_name = f"{prefix}{basename_without_ext}{suffix}.webp"
            new_path = f"{work_path}/{new_name}"
            with Image.open(file) as img:
                img.save(new_path, 'WEBP', quality=quality)

            res_list.append(new_path)
            print(Ansi.blend(Ansi.GREEN,
                             f"  => {new_path}"
                             ))
        return wf_msg

    return func
