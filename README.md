# Chain of thought is all you need

A project of multi-model dataset reinforcement and pre-training of large-scale multimodal reasoning.


**Motivation**: 

- To address the limitations of existing models: proposing new methods and technologies to overcome these limitations in multimodal large-scale models in reasoning tasks and description generation processes.
- Potential application scenarios: the successful application of improved models can bring improvement to related industries, such as autonomous driving, intelligent monitoring, virtual assistants, etc., thus generating broader social and economic value.
- Promoting technological innovation: by constructing new datasets, developing new pre-training objectives, loss functions and other methods, new research directions and technological breakthroughs can be brought to the fields of computer vision and natural language processing.
- Improving the interpretability of artificial intelligence: by improving the reasoning ability of the model, it enables artificial intelligence systems to generate more reasonable and consistent explanations when dealing with complex tasks, thereby improving their interpretability.

[PaperList](https://docs.qq.com/sheet/DQ0FmVURmYmFIVmtV?scene=b38db4adca404be50932e954FZWrp1&tab=BB08J2)

## Contribution

![Downloads](https://github.com/Jananzzzz/CoT-is-all-you-need/files/11635889/chain-of-thought.zip)

- Build a dataset that includes visual reasoning with causal chains to provide valuable resources for relevant research. 
- Adjust the pre-training objectives during representation learning to enable the model to handle reasoning tasks. 
- Optimize model performance by introducing strategies such as multi-task loss functions and additional loss functions. 
- Propose an approach to evaluate the rationality and consistency of generated text in causal chains.

### Dataset

- coco
- gqa
- sbu_captions
- Visual Genome(VG)
- CC 3M
- CC12MM
- Laion 14M

### Ideas for data construction

The seven datasets mentioned above all contain images and text. However, the text does not meet the research needs, so it needs to be reorganized. The idea is as follows:

- Research existing visual reasoning models, use existing images to freely generate logical reasoning capabilities (including objects in the picture, the meaning of the picture, etc.), generate data for each image, and research filtering methods to filter the generated data.

- JSON file format (using coco as an example):
```
[
    {"COT_Text": "", "image": "", "image_id": ""},
    {"COT_Text": "", "image": "", "image_id": ""},
    {"COT_Text": "", "image": "", "image_id": ""}
]
[
    {
        "question_id":458752000,
        "question":"What is this photo taken looking through?",
        "caption":"What is this photo taken looking through? ### 1. This is an image of a baseball game in a park with a player throwing a ball and another running to catch it.2. The image is taken from a perspective that is behind the catcher.3. The image is taken through the catcher’s glove. $$$ This photo is taken looking through the catcher’s glove.",
        "image":"train2014/COCO_train2014_000000458752.jpg",
        "dataset":"vqa",
        "image_id":"coco_458752",
        "hint1":"###",
        "hint2":"$$$"
    }
    {
        "image":"image/1.jpg",
        "caption":"trees line the sidewalk. ### 1. This is an image of a street with a couple of men standing on a sidewalk.2. The men are wearing jackets, one of them is wearing a red jacket and the other is wearing a black jacket.3. There is a white truck parked on the side of the road.4. There is a green pole with a sign on it.5. There is a clock with a green frame.6. The sidewalk is made of concrete.7. The street is lined with trees on both sides.8. The trees have no leaves, indicating that the photo was taken in the winter.9. The trees are tall and thin, with branches that are bare.10. The trees are evenly spaced along the sidewalk.11. The trees provide a natural barrier between the sidewalk and the street.12. The trees add a natural element to the urban environment.13. The trees are a reminder of the changing seasons.14. The trees are a symbol of life and growth in the midst of the city. $$$ trees line the sidewalk.",
        "image_id":"vg_1",
        "dataset":"vg"
    }
]
```
Text after "###" is the generated chain-of-thought.

## Reference

[1] Wu, Chenfei, et al. "Visual chatgpt: Talking, drawing and editing with visual foundation models." arXiv preprint arXiv:2303.04671 (2023).

[2] Shen, Yongliang, et al. "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace." arXiv preprint arXiv:2303.17580 (2023).

[3] https://github.com/microsoft/visual-chatgpt



## Contributing

We welcome contributions from anyone interested in improving or expanding upon this project. If you would like to contribute, please fork this repository and submit a pull request.