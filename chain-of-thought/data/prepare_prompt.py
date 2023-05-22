import json
# old json
old_json_example = {
    "image_id": 299024,
    "chain-of-thought": " it seems that the scene in the picture is a city street with stop signs and street signs in the background. The stop sign is located in the center of the street, which suggests that there is a road or path that the person is walking down, and the street sign is located on the right side of the road, which means that the person is going towards that specific place. The relationship between the stop and street signs is that they are used to guide traffic to a specific place, which means that they are important for ensuring safe traffic flow. The significance of the stop sign and street sign in the context of traffic management is to help ensure safe traffic flow, which means that they are important for the overall well-being of the city.",
    "caption": "a stop sign sitting next to a street sign"
}

# new json
new_json_example = {
    "img": "000000299024.jpg",
    "prompt": "what is the caption of this image?",
    "label": "a stop sign sitting next to a street sign",
}

# convert old json to new json
with open("D:/CoT-is-all-you-need/chain-of-thought/data/chain-of-thought.json", "r") as f:
    data = json.load(f)

for sample in data:
    sample["img"] = f"{sample['image_id']:012d}.jpg"
    sample["prompt"] = "what is the caption of this image?"
    sample["label"] = sample["caption"]
    del sample["image_id"]
    del sample["chain-of-thought"]
    del sample["caption"]
    
with open("D:/CoT-is-all-you-need/chain-of-thought/data/chain-of-thought.json", "w") as f:
    json.dump(data, f, indent=4)

