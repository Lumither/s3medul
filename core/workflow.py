import importlib
from pathlib import Path

from pandas import DataFrame

from .ansi import Ansi


def set_mime(wf_msg):
    ext = Path(wf_msg["wf_work_path"]).suffix[1:]
    mime_db: DataFrame = wf_msg["wf_mime_db"]
    res = mime_db[mime_db["ext"].str.fullmatch(ext, case=False, na=False)]["typ"].tolist()
    if len(res) < 1:
        raise Exception("Unknown file type")
    mime = res[0]
    wf_msg["wf_mime"] = mime
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
            print(Ansi.blend(Ansi.YELLOW, f"  => Using default {t1} workflow"))
            return base_module.workflow
        except ModuleNotFoundError:
            raise Exception(f"Unsupported file type (workflow not found): '{mime_type}'")
