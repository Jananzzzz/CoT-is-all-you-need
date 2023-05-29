from pygtrans import Translate
import json

cot_list = []
caption_list = []
id_list = []

with open("chain-of-thought.json") as f:
    data = json.load(f)
for i in data:
    cot_list.append(i["chain-of-thought"])
    caption_list.append(i["caption"])
    id_list.append(i["image_id"])

print(len(cot_list))
print(len(caption_list))
print(len(id_list))

client = Translate()
translation0 = client.translate(cot_list)
translation1 = client.translate(caption_list)


cot = []
# write to a new file:
with open("chain-of-thought-translated.json", "w") as f:
    for i in range(len(id_list)):
        cot.append({"image_id": id_list[i], "chain-of-thought": translation0[i].translatedText, "caption": translation1[i].translatedText})
    json.dump(cot, f, indent=4, ensure_ascii=False)