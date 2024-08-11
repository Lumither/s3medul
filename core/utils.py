from pathlib import Path

from pandas import DataFrame


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:.2f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def ensure_list(element):
    if isinstance(element, list):
        return element
    return [element]


def get_file_mime(mime_db: DataFrame, f_path: str) -> str:
    ext = Path(f_path).suffix[1:]
    res = mime_db[mime_db["ext"].str.fullmatch(ext, case=False, na=False)]["typ"].tolist()
    if len(res) < 1:
        raise Exception("Unknown file type")
    return res[0]
