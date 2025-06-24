import requests
import json

# Object ID from the Met
object_id = "845141"

# Met API URL
url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"

# Get the data
response = requests.get(url)
data = response.json()

# Save it locally as a .json file
with open(f"{object_id}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Metadata for object {object_id} saved as {object_id}.json")
