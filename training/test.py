import argparse
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
from model import chat, VisualGLMModel

model, model_args = VisualGLMModel.from_pretrained("/root/autodl-tmp/.sat_models/visualglm-6b", args=argparse.Namespace(fp16=True, skip_init=True))




from sat.model.mixins import CachedAutoregressiveMixin
model.add_mixin('auto-regressive', CachedAutoregressiveMixin())


while True:
    image_id = input("input your image id: ")
    image_path = f"/root/autodl-tmp/training_data/images/000000{image_id}.jpg"
    prompt = input("input your prompt: ")
    response, history, cache_image = chat(image_path, model, tokenizer, prompt, history=[])
    print(response)