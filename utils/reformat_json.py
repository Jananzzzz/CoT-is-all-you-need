import json

with open('./data/coco2017/annotations(old)/captions_train2017.json') as f_in, open('./data/coco2017/annotations/captions_train2017.json', 'w') as f_out:
    data = json.load(f_in)
    json.dump(data, f_out, indent=4)
f_in.close()
f_out.close()

with open('./data/coco2017/annotations(old)/captions_val2017.json') as f_in, open('./data/coco2017/annotations/captions_val2017.json', 'w') as f_out:
    data = json.load(f_in)
    json.dump(data, f_out, indent=4)
f_in.close()
f_out.close()

with open('./data/coco2017/annotations(old)/instances_train2017.json') as f_in, open('./data/coco2017/annotations/instances_train2017.json', 'w') as f_out:
    data = json.load(f_in)
    json.dump(data, f_out, indent=4)
f_in.close()
f_out.close()

with open('./data/coco2017/annotations(old)/instances_val2017.json') as f_in, open('./data/coco2017/annotations/instances_val2017.json', 'w') as f_out:
    data = json.load(f_in)
    json.dump(data, f_out, indent=4)
f_in.close()
f_out.close()

with open('./data/coco2017/annotations(old)/person_keypoints_train2017.json') as f_in, open('./data/coco2017/annotations/person_keypoints_train2017.json', 'w') as f_out:
    data = json.load(f_in)
    json.dump(data, f_out, indent=4)
f_in.close()
f_out.close()

with open('./data/coco2017/annotations(old)/person_keypoints_val2017.json') as f_in, open('./data/coco2017/annotations/person_keypoints_val2017.json', 'w') as f_out:
    data = json.load(f_in)
    json.dump(data, f_out, indent=4)
f_in.close()
f_out.close()































