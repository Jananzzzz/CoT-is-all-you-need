# read json as data list
import json

bad_data = 0

with open('./chain-of-thought/chain-of-thought.json') as f:
    data = json.load(f)

for i in data:
    if len(i["chain-of-thought"]) < 5:
        print(i["chain-of-thought"])
        bad_data += 1

print(bad_data)
