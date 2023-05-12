import string
import json
import time

def word_count(type):
    sentence_list = []
    words = []
    with open("D:\CoT-is-all-you-need\chain-of-thought\chain-of-thought.json") as f:
        data = json.load(f)
        for i in range(len(data)):
            sentence_list.append(data[i][f'{type}'])
    
    for sentence in sentence_list:
        text = sentence.lower() 
        # first remove the punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # split text into words
        words += text.split()
    
    start_time = time.time()

    unique_words = set(words)
    word_counts = {}
    for word in unique_words:
        word_counts[word] = words.count(word)
    
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    end_time = time.time()

    for i in range(500):
        print(sorted_word_counts[i])
    
    print("Time taken: ", end_time - start_time)
    return sorted_word_counts
    
# word_count('chain-of-thought')
# print("-------------------------------------------------------------")
word_counts = word_count('caption')

# import matplotlib.pyplot as plt

# x_bar = []
# y_bar = []
# for i in range(len(word_counts)):
#     x_bar.append(word_counts[i][0])
#     y_bar.append(word_counts[i][1])

# refined_x_bar = []
# refined_y_bar = []

# def is_square_number(n):
#     return n**0.5 == int(n**0.5)

# for i in range(len(x_bar)):
#     if is_square_number(i):
#         refined_x_bar.append(x_bar[i])
#         refined_y_bar.append(y_bar[i])


# # plt.bar(x_bar, y_bar, color='green') # bar chart
# plt.plot(refined_x_bar, refined_y_bar, color='green') # line chart
# plt.xlabel("Words")
# plt.ylabel("Frequency")
# plt.show()
