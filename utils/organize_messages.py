question_list = [
    "what is the color of the ball?",
    "what is the color of the glove?",
    "what is the color of the bat?",
    "what is the color of the uniform?",
    "what is the color of the hat?",
    "what is the color of the shoes?",
    "what is the color of the pants?",
    "what is the color of the shirt?", 
    "what is the color of the socks?",
    "what is the color of the helmet?"
]
answer_list = [
    "white",
    "black",
    "black",
    "white",
    "black",
    "black",
    "white",
    "white",
    "white",
    "black" 
]
caption = "cat on sofa"
organize_message = [
    {
    "role": "user",
    "content":
    f"""imagine you are a person with strong reasoning ability. 
Given question-answering pairs, use your reasoning ability to extract useful \
infomartion to get the final result.
Both question-answering pairs and final results are provided below:
```
question: "{question_list[0]}" Answer: "{answer_list[0]}."
question: "{question_list[1]}" Answer: "{answer_list[1]}."
question: "{question_list[2]}" Answer: "{answer_list[2]}."
question: "{question_list[3]}" Answer: "{answer_list[3]}."
question: "{question_list[4]}" Answer: "{answer_list[4]}."
question: "{question_list[5]}" Answer: "{answer_list[5]}."
question: "{question_list[6]}" Answer: "{answer_list[6]}."
question: "{question_list[7]}" Answer: "{answer_list[7]}."
question: "{question_list[8]}" Answer: "{answer_list[8]}."
question: "{question_list[9]}" Answer: "{answer_list[9]}."
Final result: {caption}
```
Your output  should be a list of useful infomation related to the final result."""
    }
]

test_message = {
    "role": "user",
    "content": f"""imagine you are a person with strong reasoning ability. 
Given question-answering pairs, use your reasoning ability to extract useful \
infomartion to get the final result. 
Both question-answering pairs and final results are provided below:
'''
"""
}

# add 5 questions and answers to test_message
for i in range(5):
    test_message["content"] += f"""question: '{question_list[i]}' Answer: '{answer_list[i]}.'
"""

test_message["content"] += f"""Final result: {caption}
'''
Your output  should be a list of useful infomation related to the final result."""

print(organize_message[0]["content"])
print(test_message["content"])