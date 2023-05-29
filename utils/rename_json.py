import json
with open("chain-of-thought-translated.json") as f:
    data = json.load(f)
    for i in data:
        i["图片ID"] = i.pop("image_id")  
        i["思维链"] = i.pop("chain-of-thought")
        i["标题"] = i.pop("caption")

with open("思维链.json", "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)