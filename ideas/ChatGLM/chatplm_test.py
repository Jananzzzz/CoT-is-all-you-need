from transformers import AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM
from pycocotools.coco import COCO
import re
import json
import time
import random
import torch
from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

def translator(input_text):

    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
    
    text = input_text

    # input_text = """The scene in the picture could be one of the most exciting tennis matches of all time, with two men(Players) playing against each other in a serve-and-serve场地. The men are both tall and strong, and their skills and策略 are likely to be key to the outcome of the match. The serve-and-serve场地 in the background adds to the sense of excitement and action, as the men are trying to outdo each other with their serve's. The use of "Double tennis match" highlights the unique nature of the match, as it involves two players(Players) on opposite sides of the court. The overall scene could be one of intense competition and passion, with the men's skills and energy driving the match."""

    def translate(text_to_translate):
        input_ids = tokenizer(text_to_translate, return_tensors="pt").input_ids
        outputs = model.generate(input_ids=input_ids)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    all_chinese_words = re.findall("[\u4e00-\u9fff]+", text)
    chinese_words = []
    for word in all_chinese_words:
        if word not in chinese_words:
            chinese_words.append(word)

    for word in chinese_words:
        replacement = " "+translate(word).lower()
        replacement = replacement.replace(".", "")
        text = text.replace(word, replacement)

    text = text.replace("，", ",")
    text = text.replace("。", ".")

    return text

def contain_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fff]')  # Unicode range for Chinese characters
    return bool(re.search(pattern, text))

def refine_text(text):
    text = text.replace("Based on the information given,", "")
    text = text.replace("base on the information given,", "")
    text = text.replace("Based on the information provided,", "")
    text = text.replace("based on the information provided,", "")
    text = text.replace("Based on the information,", "")
    text = text.replace("based on the information,", "")
    text = text.replace("Based on the information", "")
    text = text.replace("based on the information", "")
    text = text.replace("\\", "")
    return text

def visual_question_answering(image_path, question_list):
    # prepare image + question
    # image = Image.open("D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg")
    image = Image.open(image_path)
    question_list = question_list
    answer_list = []

    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    vqa_model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    # check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # move model and inputs to GPU
    vqa_model.to(device)

    for question in question_list:
        encoding = processor(image, question, return_tensors="pt").to(device)

        # forward pass
        with torch.no_grad():
            outputs = vqa_model(**encoding)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            answer_list.append(vqa_model.config.id2label[idx])

    return answer_list

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
    prompt = f"""Convert each pair of question-answer below to a statement sentence:
'''      
"""      
    for i in range(len(question_list)):
        prompt += f"""question{i+1}: '{question_list[i]}'   Answer{i+1}: '{answer_list[i]}.'
"""      
    prompt += f"""'''      
Output a list of statement sentences."""

    organize_question_answering_history = [
        ('Convert each pair of question-answer below to a statement sentence:\n```\nquestion1: "what is the purpose of the sun bear eating a carrot on a rock?" Answer1: "Satisfy hunger."\nquestion2: "what type of food is the sun bear eating?" Answer2: "Carrot."\nquestion3: "How was the sun bear able to find a carrot on a rock?" Answer3: "Yes."\nquestion4: "Where is the sun bear from?" Answer4: "Africa."\nquestion5: "Why is the sun bear on a rock?" Answer5: "Resting."\n```\nOutput a list of statement sentences.', '1. The purpose of the sun bear eating a carrot on a rock is to satisfy hunger.\n2. The sun bear is eating a carrot.\n3. The sun bear is able to find a carrot on a rock.\n4. The bear is from africa.\n5. The bear is resting on a rock.')
    ]
    response, history = model.chat(tokenizer, prompt, history=organize_question_answering_history)
    return response

def organize_information(statement):
    prompt = f"""Here is a caption: "{caption}".
Below are some statements that related to the caption.
{statement}
Please identify which information can deduce the caption, output in a list without any other prompt or prefix.
"""      

    response, history = model.chat(tokenizer, prompt, history=[])
    return response

def form_the_chain(information_list):
    prompt = f"""You are provided with a list of information of a picture:
"""
    for idx, info in enumerate(information_list):
        prompt += f"""{idx+1}. {info}
"""
    prompt += f"""Using logic thinking to reason out scene of the picture."""
    form_the_chain_history = [
        ('You are provided with a list of information of a picture.\ninformation1: the man is bald.\ninformation2: he is wearing a black suit.\ninformation3: he is standing on a skateboard.\ninformation4: he is not actively skateboarding, but just standing on the skateboard.\nUsing logic thinking to reason out scene of this picture.', 'The man is bald, wearing a black suit, and standing on a skateboard. He is not actively skateboarding, but he is standing on the skateboard for some reason. The man is in a city or town, and there are other people in the background as well. Some of the people in the background may be walking, drinking coffee or other activities. The man\'s skateboard may be in the center of his feet, and he is looking around him at the city or town he is in. There may be other objects such as buildings, cars, or streets in the background as well. There may be a feeling of excitement or adventure in the man\'s mind, as he is standing on a skateboard in a city.'),
        ('You are provided with a list of information of a picture.\ninformation1: the person is walking.\ninformation2: there is a traffic light in the image.\ninformation3: the person is not crossing the street in a hurry.\nUsing logic thinking to reason out scene of this picture.',"It is likely that the person in the picture is walking down a street, across from a traffic light. The traffic light is in the image, which suggests that there is a road or path that the person is walking down, and the person is not in a hurry, so it seems that they are taking their time and enjoying the scenery. The person's walking suggests that they are on their way to/from something, and the lack of a hurry suggests that they are not in a rush to get there. The overall scene could be one of tranquility and peace, as the person is walking down a street with a traffic light in the background."),
        ('You are provided with a list of information of a picture.\ninformation1: a woman and a dog sitting on the beach playing a game.\ninformation2: the woman is sitting on the ground with her back to the camera, while the dog is sitting next to her, looking up at her with a curious expression.\nThe sun is setting in the background, casting a warm, golden light on the scene.\nUsing logic thinking to reason out scene of this picture.', 'The caption for this image is meant to highlight the bond and playfumess benween thewoman and her dog. The fact that they are playing a game together on the beach suggests that they have a close relationshie and enjoy spending time together, The sunset in the background adds to the sense of warmth and nostalgia'),
        ('You are provided with a list of information of a picture.\ninformation1: a lamp is in the center of the room.\n information2: a bed located in the left side of the room.\nUsing logic thinking to reason out scene of this picture.','because the lamp is in the center of the room, and the there are two beds in two sides of the room. Based on the information, it is possible that the lamp is between the two beds.')
    ]
    response, history = model.chat(tokenizer, prompt, history=form_the_chain_history)
    return response

def translate_to_english(response_text):
    prompt = f"""Below is a output of a langauage model:
{response_text}
It may contain some Chinese characters. Please translate the Chinese characters to English.
Your output will be the tranlated version."""
    response, history = model.chat(tokenizer, prompt, history=[])
    return response

if __name__ == "__main__":
    
    # model
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

    # data
    data_dir = '/root/autodl-tmp/COCO2017'
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
    for _ in range(500):

        Start_time = time.time()

        item = data[random.randint(0, len(data))]

        image_id = item['image_id']
        caption = item['caption']
        picture_path = item['image_path']

        # image_id = 458752
        # caption = "a baseball pitcher winds up to pitch the ball."
        # picture_path = "D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg"

        print(f"Image {i}: ", caption)
        print(picture_path)

        # generate questions
        start_time = time.time()
        response_text = generate_question(caption) # return questions
        print(response_text)
        question_list = []
        for line in response_text.split('\n'):
            if line:
                question_list.append(line[2:])
        end_time = time.time()
        print(f"Generate questions consumed : {end_time - start_time} seconds.")
        print("")

        # answer questions
        start_time = time.time()
        answer_list = visual_question_answering(picture_path, question_list) # return a list of answers
        for i in range(len(question_list)):
            print(question_list[i], answer_list[i])
        end_time = time.time()
        print(f"Answer questions consumed : {end_time - start_time} seconds.")
        print("")

        # organize question answering to information list
        start_time = time.time()
        response_text = organize_question_answering(question_list, answer_list) # return statements
        print(response_text)
        information_list = []
        for line in response_text.split('\n'):
            if line:
                information_list.append(line)
        end_time = time.time()
        print(f"Organize question answering consumed : {end_time - start_time} seconds.")
        print("")

        # form the chain
        start_time = time.time() 
        chain_of_thought = form_the_chain(information_list) # return chain of thought
        print(chain_of_thought)
        end_time = time.time()
        print(f"Form the chain consumed : {end_time - start_time} seconds.")
        print("")

        # check whether contain chinese character
        if contain_chinese(chain_of_thought):
            print("Contain chinese character, translate to english.")
            start_time = time.time()
            result = translator(chain_of_thought) # final result
            end_time = time.time()
            print(f"translating consumed: {end_time - start_time} seconds.")
        else:
            result = chain_of_thought # final result

        # refine the text
        result = refine_text(result)

        # print final result
        print(result)
        print("")

        with open('/root/chain-of-thought/chain-of-thought.json', 'r+') as f:
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
        
        End_time = time.time()
        print(f"Total image&Caption {_} processing consumed : {End_time - Start_time} seconds.")
        print("")
        