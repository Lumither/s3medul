from core.actions.push_s3 import push_s3
from core.actions.register import func_reg_name, copy

workflow = [
    copy("main.orig_path", func_reg_name(push_s3, 'in')),
    push_s3
]
