from pycocotools.coco import COCO
import numpy as np
import json

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
