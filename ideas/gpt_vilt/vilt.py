from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import torch

def visual_question_answering(image_path, question):

    # prepare image + question
    # image = Image.open("D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg")
    image = Image.open(image_path)

    question = question

    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    # # prepare inputs
    # encoding = processor(image, question, return_tensors="pt")

    # # forward pass
    # outputs = model(**encoding)
    # logits = outputs.logits
    # idx = logits.argmax(-1).item()
    # return model.config.id2label[idx]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # move model and inputs to GPU
    model.to(device)
    encoding = processor(image, question, return_tensors="pt").to(device)

    # forward pass
    with torch.no_grad():
        outputs = model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        return model.config.id2label[idx]

# print(visual_question_answering("D:/CoT-is-all-you-need/data/coco2017/train2017/000000458752.jpg", "what is the color of the ball?"))