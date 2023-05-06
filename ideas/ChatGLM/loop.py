from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

prompt_example = """
An example of reasoning:
input (caption of image): "a lamp that is between two beds."
input (information of image): "The lamp is located in the center of the image.", "there are two beds in the room."
output (reason based on the input): because there is a lamp located in the center of the image, and there are two beds in the room, so the lamp is possibly located between two beds, which is correspond to the caption.

now given input of (caption of image) and (information of image), please imitate the reasoning statement above to deduce the final caption. Give your output.
input (caption of image): "A woman sitting at a table topped with pizzas."
input (information of image): "the woman is sitting at the table.", "there are some pizzas on the table.", "the woman is alone."
"""

# while(True):
#     prompt = input("input your prompt:")
#     response, history = model.chat(tokenizer, prompt, history=[])
#     print(response)
#     print("")

history = []

while(True):

    print("Enter your prompt:")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

    prompt = '\n'.join(lines)


    response, history = model.chat(tokenizer, prompt, history=history)
    print(response)
    print("")
    history = history
    print(history)