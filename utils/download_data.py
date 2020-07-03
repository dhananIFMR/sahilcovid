import os
import json

import requests


google_sheet_code = "1i3Gvg0iGgPZbD4ClaLo55INProMnk2DaoSFh_AjgpUQ"
sheet_page_number = 1

while True:
    resp = requests.get(
        f"https://spreadsheets.google.com/feeds/cells/{google_sheet_code}/{sheet_page_number}/public/full?alt=json"
    )
    if resp.status_code != requests.codes.ok:
        break
    data = resp.json()
    title = data["feed"]["title"]["$t"]
    entries = [x["gs$cell"] for x in data["feed"]["entry"]]
    [x.pop("inputValue") for x in entries]
    with open(f"./static/data/{title}.json", "w") as f:
        json.dump(entries, f)
    print(title)
    sheet_page_number += 1
