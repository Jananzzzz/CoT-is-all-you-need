import openai
from vilt import visual_question_answering
from pycocotools.coco import COCO
import json
import time
import random

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
            'image_id': imgId,
            'image_path': f"{data_dir}/{data_type}/{imgData['file_name']}",
            'caption': caption['caption']
        }
        data.append(pair)


for i in range(500):

    item = data[random.randint(0, len(data))]

    image_id = item['image_id']
    caption = item['caption']
    picture_path = item['image_path']

    # image_id = 458752
    # caption = "a baseball pitcher winds up to pitch the ball."
    # picture_path = "D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg"

    print(caption)
    print(picture_path)

    try:

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
            print(question)
            question_list.append(question)
        print("")

        answer_list = []
        for idx,question in enumerate(question_list):
            answer_list.append(visual_question_answering(picture_path, question))
            print(idx, question, answer_list[idx])
        print("")


        organize_message = [{
            "role": "user",
            "content": f"""imagine you are a person with strong reasoning ability. 
Given question-answering pairs, use your reasoning ability to extract useful \
infomartion to get the final result. 
Both question-answering pairs and final results are provided below:
'''      
"""      
        }
        ]

        # add 5 questions and answers to test_message
        for i in range(len(question_list)):
            organize_message[0]["content"] += f"""question: '{question_list[i]}' Answer: '{answer_list[i]}.'
"""      

        organize_message[0]["content"] += f"""Final result: {caption}
'''      
Your output should be a list of statement sentences of useful infomation related to the final result, without any prefix or prompt."""

        print("")
        print(organize_message[0]["content"])
        print("")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=organize_message,
            temperature=0.9,
        )

        print(response.choices[0]['message']['content'])
        print("")

        refine_message = [
            {
                "role": "user",
                "content": f"""Here is a caption: "{caption}".
Below are some information that related to the caption.
Please identify which information can deduce the caption, output in a list without any other prompt or prefix.
"""      
            }
        ]

        for info in response.choices[0]['message']['content'].splitlines():
            refine_message[0]["content"] += f"""{info}
"""      

        print(refine_message[0]["content"])

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=refine_message,
            temperature=0.9,
        )

        print(response.choices[0]['message']['content'])

        results = []
        for result in response.choices[0]['message']['content'].splitlines():
            results.append(result[2:])
        
        with open('D:/CoT-is-all-you-need/ideas\gpt_vilt/chain-of-thought.json', 'r+') as f:
            thoughts = json.load(f)
            new_thought = {
                "image_id": image_id,
                "caption": caption,
                "chain-of-thought": results
            }
            thoughts.append(new_thought)
            f.seek(0)
            json.dump(thoughts, f, indent=4)
            f.truncate()


        end_time = time.time()
        print(f"this image-caption chain of thought reasoning costed : {end_time - start_time} seconds")
        print("")

        # if (end_time - start_time) < 60:
        #     time.sleep(61 - (end_time - start_time))
        time.sleep(60)


        print(f"Chain of thought reasoning for {caption} finished.")

    except Exception as e:
        print(e)
        print(f"Chain of thought reasoning for {caption} failed.")
        time.sleep(60)

