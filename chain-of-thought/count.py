# read json as data list
import json

total = 0
bad_data = 0
image_list = []
caption_list = []


with open('./chain-of-thought/chain-of-thought.json') as f:
    data = json.load(f)

for i in data:
    total += 1
    if len(i["chain-of-thought"]) < 5:
        bad_data += 1
    if i["image_id"] not in image_list:
        image_list.append(i["image_id"])
    if i["caption"] not in caption_list:
        caption_list.append(i["caption"])

print(f"There are {total} pieces of data in total.")   # 10254
print(f"There are {bad_data} pieces of bad data.")   # 4
print(f"There are {len(image_list)} images in total.")    # 8067    
print(f"There are {len(caption_list)} captions in total.")   # 8053




