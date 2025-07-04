import requests
import json

object_id = 752041
url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"

response = requests.get(url)
data = response.json()

filename = f"{object_id}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Metadata for object {object_id} saved as {filename}")
