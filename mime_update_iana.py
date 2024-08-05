import pandas as pd

categories = [
    "application",
    "audio",
    "font",
    "haptics",
    "image",
    "message",
    "model",
    "multipart",
    "text",
    "video",
]

source = "https://www.iana.org/assignments/media-types/{c}.csv"

mime_csv = pd.DataFrame(columns=["ext", "typ"])

cnt = 1

for ctgy in categories:
    url = source.format(c=ctgy)
    print(f"({cnt}/{len(categories)}) Working on {url}... ", end="", flush=True)
    try:
        data = pd.read_csv(url, sep=",")
        extract = data[["Name", "Template"]].rename(
            columns={"Name": "ext", "Template": "typ"}
        )
        mime_csv = pd.concat([mime_csv, extract], ignore_index=True)
    except Exception as e:
        print("\033[91mERROR\033[0m")
        print(f"    => url: {url}")
        print(f"    => {e}")
    else:
        print("\033[92mSUCCESS\033[0m")
    cnt += 1

mime_csv.to_csv("~/.s3medul/mime.csv", index=False)
