import json

with open("./data/coco2017/annotations/captions_train2017.json", "r") as f:
    data = json.load(f)
    # extract all captions into a list
    captions = [x["caption"] for x in data["annotations"]]
    # save list into a file
f.close()

for i in range(10):
    print(captions[i])

with open("./data/all_train_captions/captions.txt", "w") as f:
    for caption in captions:
        f.write(caption + "\n")
f.close()





