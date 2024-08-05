import pandas as pd
import requests

source = "https://cdn.jsdelivr.net/gh/jshttp/mime-db@master/db.json"

mime_csv = []

print(f" Working on {source}... ", end="", flush=True)
try:
    res = requests.get(source)
    res.raise_for_status()
    data = res.json()

    for (mime, val) in data.items():
        if (extensions := val.get("extensions")) is not None:
            for ext in extensions:
                mime_csv.append({"ext": ext, "typ": mime})
except Exception as e:
    print("\033[91mERROR\033[0m")
    print(f"    => url: {source}")
    print(f"    => Error: {e}")
else:
    print("\033[92mSUCCESS\033[0m")

pd.DataFrame(mime_csv).to_csv("~/.s3medul/mime.csv", index=False)
