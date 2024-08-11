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
