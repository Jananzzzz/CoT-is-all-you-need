import openai
import config

openai.api_key = config.openai_api

question_generate_message = [
    {
    "role": "user", 
    "content": 
    """I am developing an AI model for image caption reasoning. \
You need to generate questions based on the given caption of image, \
so i can use the questions to train and build AI models of visual question answering. Your output should be a list."""
    },
]

caption = "a baseball pitcher winds up to pitch the ball."

question_generate_message.append({"role": "user", "content": f"{caption}"})

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=question_generate_message,
    temperature=0.9,
)

question_response = response.choices[0]['message']['content']
question_list = []
for question in question_response.splitlines():
    question_list.append(question[3:])


answer_list = []

organize_message = [
    {
    "role": "user",
    "content":
    f"""
imagine you are a person with strong reasoning ability. 
Given question-answering pairs, use your reasoning ability to extract useful 
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
Final result: A woman sitting at a table topped with pizza.
```
Your output  should be a list of useful infomation related to the final result.
 
    """
    }
]
