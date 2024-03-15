import requests
import json
from tqdm import tqdm
import re
from time import sleep
import ast
from tags import all_tags

API = "https://steamspy.com/api.php"
CSV_HEADERS = ["AppID", "Name", "Tag", "Developers", "Publishers",
               "Positive Reviews", "Negative Reviews", "Median Owners", "Average Playtime", "Median Playtime",
               "CCU", "Price", "Initial Price", "Discount"
]
TAGS_TO_REQUEST = all_tags
FILE = "more_games.csv"


def request(tag: str=None) -> object:
    if tag == None:
        raise ValueError("Please enter a tag")
    response = requests.get(API+f"?request=tag&tag={tag}")
    if response.status_code != 200: return None
    decoded = response.content.decode(encoding="utf-8")
    if not decoded: return None
    return json.loads(decoded)

print("Requesting information...")
data_array = {}
progress = tqdm(range(len(TAGS_TO_REQUEST)))
for tag in TAGS_TO_REQUEST:
    requested = request(tag)
    if not requested or requested == {}:
        sleep(1)
        progress.update()
        continue
    data_array[tag] = requested
    sleep(1)
    progress.update()
progress.close()

print("Evaluating data...")
checked_data_duplication: dict[str, list[str]] = {}
progress = tqdm(range(sum([len(data_array[tag]) for tag in data_array])))
for tag in data_array:
    for key in data_array[tag]:
        data = data_array[tag][key]
        owners = data["owners"].replace(",", "").split(" .. ")
        clean = re.compile(r'[^a-zA-Z\s]')
        name = re.sub(clean, '', data['name']).replace('"', '')
        developer = re.sub(clean, '', data['developer'].replace('"', '')).split(", ")
        publisher = re.sub(clean, '', data['publisher'].replace('"', '')).split(", ")
        toWrite = [
            key, f"\"{name}\"", f"\"['{tag}']\"", f"\"{developer}\"", f"\"{publisher}\"",
            str(data["positive"]), str(data["negative"]), str((int(owners[0])+int(owners[1]))/2), str(data["average_forever"]), str(data["median_forever"]),
            str(data["ccu"]), str(int(data["price"])/100), str(int(data["initialprice"])/100), data["discount"]
        ]
        if key in checked_data_duplication.values():
            old_tags: list[str] = ast.literal_eval(checked_data_duplication[key][2].replace('"', ''))
            toWrite[2] = f"\"{old_tags + [tag]}\""
        checked_data_duplication[key] = toWrite
        progress.update()
progress.close()

print(f"Writing to {FILE}...")
with open(FILE, "w") as file:
    file.flush()
    file.write(",".join(CSV_HEADERS) + "\n")
    progress = tqdm(range(sum([len(data_array[tag]) for tag in data_array])))
    for key in checked_data_duplication:
        file.write(",".join(checked_data_duplication[key]) + "\n")
        progress.update()
    progress.close()
print("Done")