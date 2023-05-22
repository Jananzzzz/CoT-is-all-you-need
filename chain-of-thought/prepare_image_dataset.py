import os
import shutil
import json

source_dir = "D:/CoT-is-all-you-need/data/coco2017/train2017"
target_dir = "D:/CoT-is-all-you-need/chain-of-thought/data/images"
json_file = "D:/CoT-is-all-you-need/chain-of-thought/data/chain-of-thought.json"

image_ids = []

with open(json_file, 'r') as f:
    data = json.load(f) 
    for i in data:
        if i['image_id'] not in image_ids:
            image_ids.append(i['image_id'])
print(f"there are {len(image_ids)} images in the dataset.")
    

for i in data:
    filename = str(i['image_id']).zfill(12) + ".jpg"
    source_path = os.path.join(source_dir, filename)
    target_path = os.path.join(target_dir, filename)
    if not os.path.exists(target_path):
        shutil.copy(source_path, target_path)
    
# check how many pictrues are copied
count = 0
for filename in os.listdir(target_dir):
    if filename.endswith(".jpg"):
        count += 1

print(f"there are {count} images in the target directory.")
    