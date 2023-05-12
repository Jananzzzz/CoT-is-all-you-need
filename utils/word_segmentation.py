import string
import json
import time

chain_of_thought = []
caption = []
chain_of_thought_words = []
caption_words = []

with open("D:\CoT-is-all-you-need\chain-of-thought\chain-of-thought.json") as f:
    data = json.load(f)
    for i in range(len(data)):
        chain_of_thought.append(data[i]['chain-of-thought'])
        caption.append(data[i]['caption'])

for thought in chain_of_thought:
    text = thought.lower() 
    # first remove the punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # split text into words
    words = text.split()
    for word in words:
        chain_of_thought_words.append(word)

start_time = time.time()

unique_cot_words = set(chain_of_thought_words) # 10298
word_counts = {}
for word in unique_cot_words:
    word_counts[word] = chain_of_thought_words.count(word)

sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

end_time = time.time()


for i in range(500):
    print(sorted_word_counts[i])

print("Time taken: ", end_time - start_time)
