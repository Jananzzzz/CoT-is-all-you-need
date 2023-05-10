from transformers import AutoTokenizer, AutoModel
from pycocotools.coco import COCO
import json
import time
import random
import torch
from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

def visual_question_answering(image_path, question):
    # prepare image + question
    # image = Image.open("D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg")
    image = Image.open(image_path)
    question = question

    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    vqa_model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    # check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # move model and inputs to GPU
    vqa_model.to(device)
    encoding = processor(image, question, return_tensors="pt").to(device)

    # forward pass
    with torch.no_grad():
        outputs = vqa_model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        return vqa_model.config.id2label[idx]


def generate_question(caption):
    prompt = f"""
I am developing an AI model for image caption reasoning.
You need to generate questions based on the given caption of image, so i can use the questions to train and build AI models of visual question answering.
the caption is below:
{caption}
Your output will be a list.
"""
    response, history = model.chat(tokenizer, prompt, history=[])
    return response

def organize_question_answering(question_list, answer_list):
    prompt = f"""imagine you are a person with strong reasoning ability. 
Given question-answering pairs, use your reasoning ability to extract useful \
infomartion to get the final result. 
Both question-answering pairs and final results are provided below:
'''      
"""      
    for i in range(len(question_list)):
        prompt += f"""question: '{question_list[i]}' Answer: '{answer_list[i]}.'
"""      
        prompt += f"""Final result: {caption}
'''      
Your output should be a list of statement sentences of useful infomation related to the final result, without any prefix or prompt."""

    response, history = model.chat(tokenizer, prompt, history=[])
    return response

def organize_information(statement_list):
    prompt = f"""Here is a caption: "{caption}".
Below are some information that related to the caption.
Please identify which information can deduce the caption, output in a list without any other prompt or prefix.
"""      

    for info in statement_list.splitlines():
        prompt += f"""{info}
"""      
    response, history = model.chat(tokenizer, prompt, history=[])
    return response

def form_the_chain(information_list, history):
    prompt = f"""You are provided with a list of information of a picture:
"""
    for idx, info in enumerate(information_list):
        prompt += f"""{idx+1}. {info}
"""
    prompt += f"""Using logic thinking to reason out a complete scene of this picture."""
    response, history = model.chat(tokenizer, prompt, history=history)
    return response

def align_to_list(reponse_text):
    # align to list
    prompt = f"""Below is a output of a langauage model:
{reponse_text}
The expected ouput is a list of sentences, but the actual output may not be a list. It may contain some prefixs, prompts or conclusion.
Please align the output to a list of sentences, without any prefixs, prompts or conclusion.
Your output is the aligned list of sentences."""
    response, history = model.chat(tokenizer, prompt, history=[])
    return response

def translate_to_english(response_text):
    prompt = f"""Below is a output of a langauage model:
{response_text}
It may contain some Chinese characters. Please translate the Chinese characters to English."""
    response, history = model.chat(tokenizer, prompt, history=[])
    return response

if __name__ == "__main__":
    
    # model
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
    history = [
        ('You are provided with some pieces of information of a picture.\ninformation1: the man is bald.\ninformation2: he is wearing a black suit.\ninformation3: he is standing on a skateboard.\ninformation4: he is not actively skateboarding, but just standing on the skateboard.\nUsing logic thinking to reason out a complete scene of this picture.', 'The man is bald, wearing a black suit, and standing on a skateboard. He is not actively skateboarding, but he is standing on the skateboard for some reason. The man is in a city or town, and there are other people in the background as well. Some of the people in the background may be walking，喝咖啡， or other activities. The man\'s skateboard may be in the center of his feet, and he is looking around him at the city or town he is in. There may be other objects such as buildings, cars, or streets in the background as well. There may be a feeling of excitement or adventure in the man\'s mind, as he is standing on a skateboard in a city.'),
        ('You are provided with some pieces of information of a picture.\ninformation1: the person is walking.\ninformation2: there is a traffic light in the image.\ninformation3: the person is not crossing the street in a hurry.\nUsing logic thinking to reason out a complete scene of this picture.',"Based on this information, it is likely that the person in the picture is walking down a street, across from a traffic light. The traffic light is in the image, which suggests that there is a road or path that the person is walking down, and the person is not in a hurry, so it seems that they are taking their time and enjoying the scenery. The person's walking suggests that they are on their way to/from something, and the lack of a hurry suggests that they are not in a rush to get there. The overall scene could be one of tranquility and peace, as the person is walking down a street with a traffic light in the background."),
        ('You are provided with some pieces of information of a picture.\ninformation1: a woman and a dog sitting on the beach playing a game.\ninformation2: the woman is sitting on the ground with her back to the camera, while the dog is sitting next to her, looking up at her with a curious expression.\nThe sun is setting in the background, casting a warm, golden light on the scene.\nUsing logic thinking to reason out a complete scene of this picture.', 'Based on this description, it is likely that the caption for this image is meant to highlight the bond and playfumess benween thewoman and her dog. The fact that they are playing a game together on the beach suggests that they have a close relationshie and enjoy spending time together, The sunset in the background adds to the sense of warmth and nostalgia'),
    ]

    # data
    data_dir = 'D:/CoT-is-all-you-need/data/coco2017'
    data_type = 'train2017'
    annotation_file = f'{data_dir}/annotations/captions_{data_type}.json'
    coco = COCO(annotation_file)
    imgIds = coco.getImgIds()
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

    # generate chain of thought
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

        # generate question
        response_text = generate_question(caption) # return questions
        question_list = align_to_list(response_text) # align questions to list
        answer_list = visual_question_answering(picture_path, question_list) # return a list of answers
        response_text = organize_question_answering(question_list, answer_list) # return statements
        statement_list = align_to_list(response_text) # align statements to list
        information_list = organize_information(statement_list) # return a list of information
        chain_of_thought = form_the_chain(information_list, history) # return chain of thought
        result = translate_to_english(chain_of_thought) # final result

        with open('D:/CoT-is-all-you-need/ideas/gpt_vilt/chain-of-thought.json', 'r+') as f:
            thoughts = json.load(f)
            new_thought = {
                "image_id": image_id,
                "chain-of-thought": result,
                "caption": caption,
            }
            thoughts.append(new_thought)
            f.seek(0)
            json.dump(thoughts, f, indent=4)
            f.truncate() 