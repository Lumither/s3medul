import importlib

from .ansi import Ansi
from .utils import get_file_mime


def set_mime(wf_msg):
    wf_msg["wf_mime"] = get_file_mime(wf_msg['wf_mime_db'], wf_msg['wf_orig_path'])
    return wf_msg


def set_workflow(wf_msg):
    for func in load_workflows(wf_msg["wf_mime"]):
        wf_msg = func(wf_msg)
    return wf_msg


def load_workflows(mime_type: str):
    t1, t2 = mime_type.split("/")
    try:
        base_module = importlib.import_module(f".workflows.{t1}.{t2}", __package__)
        return base_module.workflow
    except ModuleNotFoundError:
        try:
            base_module = importlib.import_module(f".workflows.{t1}.default", __package__)
            print(Ansi.blend(Ansi.YELLOW, f"  => Warning: Using default {t1} workflow"))
            return base_module.workflow
        except ModuleNotFoundError:
            raise Exception(f"Unsupported file type (workflow not found): '{mime_type}'")
