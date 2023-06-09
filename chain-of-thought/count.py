# read json as data list
import json

total = 0
bad_data = 0
image_list = []
caption_list = []
cot_list = []


with open('./chain-of-thought.json') as f:
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
    "because","since","as","likely","may","overall","therefore","thus","suggest","possib",
    "could","would","might","not known","not clear","not sure","not certain","fact","evidence",
    "relat","purpose","reason","cause","effect","result","consequence","conclude","conclusion",
    "will","support","indicat","seem","appear","consider","add","typical","common","unknown",
    "is for","symbol","reminder","feel","used as","mean"
]

chinese_reasoning_words = [
    "因为","由于","因此","所以","可能","总的来说","因而","表明","清楚","不确定","事实","证据","目的","通常","而且","意味","为了","理由","事实","总体而言","增强","进一步","而","显示","代表","例如","看作","可以","象征","为什么",
    "似乎","用于","关于", "试图", "需求", "用途", "提供", "任务", "创造", "参考", "说明", "确定", "视为", "考虑", "道理", "方式", "用作", "暗示", "主要", "常见", "关系", "看起来", "帮助", "用来", "致力于", "来看", "主要",
    "通过", "寓意","不必", "根据", "意义", "促进", "使其", "即", "这就是", "更", "原因", "导致", "从而"
]

# 表目的
purpose_words = [
    "可能","目的","为了","理由","进一步","显示","代表","可以",
    "用于","需要", "试图", "需求", "用途", "提供", "任务", "用作", "帮助", "用来", "致力于",
    "寓意","增加", "促进", "使其", "准备"
]
# 表原因
reason_words = [
    "因为","由于","因此","所以","因而","表明","清楚","不确定","事实","证据","目的","为了","理由","事实","为什么",
    "用于","需要", "试图", "需求", "用途", "提供","说明", "确定", "道理","用作","帮助", "用来","原因"
    "根据", "意义", "导致"
]
# 表结果
result_words = [
    "因此","所以","总的来说","因而","表明","清楚","不确定","意味""总体而言","显示","代表","看作","可以",
    "似乎", "说明", "确定", "暗示", "主要","关系", "看起来","用来",
    "寓意", "促进", "使其", "即", "这就是",
]
# 表预测
predict_words = [
    "可能","表明","清楚","不确定","意味","总体而言","增强","进一步","显示","代表","看作","可以","象征",
    "似乎","用于","试图", "需求", "用途","说明", "确定", "视为", "考虑", "用作", "暗示","看起来",
    "寓意", "使其",
]
# 表递进
progressive_words = [
    "可能","总的来说","而且","为了","总体而言","进一步","而","例如", "更"
    "用于","说明", "视为", "用作","看起来", "用来", "致力于", "来看", "主要",
    "通过","不必", "根据","使其", "即", "这就是","从而"
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

# check average sentence length
total_sentence_length = 0
for cot in cot_list:
    total_sentence_length += len(cot.split())

print(f"The average sentence length is {total_sentence_length/sentence_count} words.")  



# jieba word segmentation
import jieba
text_list = []
with open("./思维链.json") as f:
    data = json.load(f)
    for i in range(len(data)):
        text_list.append(data[i]['思维链'])
all_reasoning_words_chinese = 0

purpose_words_chinese = 0
reason_words_chinese = 0
result_words_chinese = 0
predict_words_chinese = 0
progressive_words_chinese = 0

for text in text_list:
    seg_list = jieba.lcut(f"{text}", cut_all=True)
    for word in seg_list:
        if word in chinese_reasoning_words:
            all_reasoning_words_chinese += 1
        if word in purpose_words:
            purpose_words_chinese += 1
        if word in reason_words:
            reason_words_chinese += 1
        if word in result_words:
            result_words_chinese += 1
        if word in predict_words:
            predict_words_chinese += 1
        if word in progressive_words:
            progressive_words_chinese += 1
        

print(f"There are {all_reasoning_words_chinese/len(cot_list)} reasoning words in each CoT in average.")  
print(f"There are {purpose_words_chinese/len(cot_list)} purpose words in each CoT in average.")
print(f"There are {reason_words_chinese/len(cot_list)} reason words in each CoT in average.")
print(f"There are {result_words_chinese/len(cot_list)} result words in each CoT in average.")
print(f"There are {predict_words_chinese/len(cot_list)} predict words in each CoT in average.")
print(f"There are {progressive_words_chinese/len(cot_list)} progressive words in each CoT in average.")


#ededed