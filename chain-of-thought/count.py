# read json as data list
import json

total = 0
bad_data = 0
image_list = []
caption_list = []
cot_list = []


with open('./chain-of-thought/chain-of-thought.json') as f:
    data = json.load(f)

for i in data:
    cot_list.append(i["chain-of-thought"])
    total += 1
    if len(i["chain-of-thought"]) < 5:
        bad_data += 1
        print(i["image_id"])
    if i["image_id"] not in image_list:
        image_list.append(i["image_id"])
    if i["caption"] not in caption_list:
        caption_list.append(i["caption"])

print(f"There are {total} pieces of data in total.")   # 10254
print(f"There are {bad_data} pieces of bad data.")   # 4
print(f"There are {len(image_list)} images in total.")    # 8067    
print(f"There are {len(caption_list)} captions in total.")   # 8053


reasoning_words = [
    "because",
    "since",
    "as",
    "likely",
    "may",
    "overall",
    "therefore",
    "thus",
    "suggest",
    "possib",
    "could",
    "would",
    "might",
    "not known",
    "not clear",
    "not sure",
    "not certain",
    "fact",
    "evidence",
    "relat",
    "purpose",
    "reason",
    "cause",
    "effect",
    "result",
    "consequence",
    "conclude",
    "conclusion",
    "will",
    "support",
    "indicat",
    "seem",
    "appear",
    "consider",
    "add",
    "typical",
    "common",
    "unknown",
    "is for",
    "symbol",
    "reminder",
    "feel",
    "used as",
    "mean"
]


# count reasoning words in each CoT
reason_count = 0

for cot in cot_list:
    for word in reasoning_words:
        if word in cot.lower():
            reason_count += 1

print(f"There are {reason_count/len(cot_list)} reasoning words in each CoT in average.")   # 6.27   

# check sentence count in each CoT, divide by "," and "."
sentence_count = 0

for cot in cot_list:
    sentence_count += cot.count(",") + cot.count(".")

print(f"There are {sentence_count/len(cot_list)} sentences in each CoT in average.")   # 10.79




