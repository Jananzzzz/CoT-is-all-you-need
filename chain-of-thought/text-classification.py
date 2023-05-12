from transformers import pipeline
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

conversation = '''Jeff: Can I train a 🤗 Transformers model on Amazon SageMaker? 
Philipp: Sure you can use the new Hugging Face Deep Learning Container. 
Jeff: ok.
Jeff: and how can I get started? 
Jeff: where can I find documentation? 
Philipp: ok, ok you can find everything here. https://huggingface.co/blog/the-partnership-amazon-sagemaker-and-hugging-face                                           
'''
caption = "A woman is crouching down ready to hit something."
chain_of_thought = "it seems that the woman is playing a game ofbattered, and she is crouching down to hit a ball with her hands. The something in the image that the woman is trying to hit is likely a ball, as the woman is striking it with her hands. The woman's purpose in striking the something is likely to get it in the hole, as she is using her crouching position to make the hit more accurate. The image suggests that the woman is having a good time and enjoying the game, as she is using her skills and determination to success. The ball is likely the main focus of the scene, as the woman is trying to hit it with all her might. Overall, the scene suggests a playful and enjoyable atmosphere, with the woman having a good time playing the game."

summary = summarizer(chain_of_thought)
print(summary)

