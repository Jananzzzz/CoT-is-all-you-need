import json
with open('./chain-of-thought/chain-of-thought.json') as f:
    data = json.load(f)

for i in data:
    if len(i["chain-of-thought"]) < 5:
        print(i["image_id"])