import openai
from vilt import visual_question_answering
from pycocotools.coco import COCO
import numpy as np
import json
import time

openai.api_key = "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"

question_generate_message = [
    {
    "role": "user", 
    "content": 
    """I am developing an AI model for image caption reasoning. \
You need to generate questions based on the given caption of image, \
so i can use the questions to train and build AI models of visual question answering. Your output should be a list."""
    },
]

data_dir = 'D:/CoT-is-all-you-need/data/coco2017'
data_type = 'train2017'
annotation_file = f'{data_dir}/annotations/captions_{data_type}.json'

coco = COCO(annotation_file)

# Get a list of all image IDs in the dataset
imgIds = coco.getImgIds()

# Load the image data and captions for each image
data = []
for imgId in imgIds:
    imgData = coco.loadImgs(imgId)[0]
    captions = coco.imgToAnns[imgId]
    for caption in captions:
        pair = {
            'image_path': f"{data_dir}/{data_type}/{imgData['file_name']}",
            'caption': caption['caption']
        }
        data.append(pair)

for i in data:

    caption = i['caption']
    picture_path = i['image_path']

    # caption = "a baseball pitcher winds up to pitch the ball."
    # picture_path = "D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg"

    print(caption)
    print(picture_path)

    start_time = time.time()

    question_generate_message.append({"role": "user", "content": f"{caption}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=question_generate_message,
        temperature=0.9,
    )

    question_response = response.choices[0]['message']['content']

    question_list = []
    for question in question_response.splitlines():
        print(question[3:])
        question_list.append(question[3:])
    print("")

    answer_list = []
    for idx,question in enumerate(question_list):
        answer_list.append(visual_question_answering(picture_path, question))
        print(idx, question, answer_list[idx])
    print("")

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
    Final result: {caption}
    ```
    Your output  should be a list of useful infomation related to the final result.
        """
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=organize_message,
        temperature=0.9,
    )

    print(response.choices[0]['message']['content'])
    print("")

    end_time = time.time()
    print(f"this image-caption chain of thought reasoing costed : {end_time - start_time} seconds")
    print("")

