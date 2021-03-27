import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision import transforms
from PIL import Image, ImageDraw
import numpy as np

import json


import matplotlib.pyplot as plt
import cv2

import os

from torch.utils.data import DataLoader, Dataset


class LunarSurfaceImageLoader(Dataset):

    def __init__(self, imgs, transform):
        # self.img_dir = img_dir
        # self.transform = transform

        # self.imgs = sorted(list(os.listdir(img_dir)))
        # for file in self.imgs:
        #     if "txt" in file:
        #         self.imgs.remove(file)
        self.imgs = [imgs]
        self.transform = transform
        
    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        #image = Image.open(os.path.join(self.img_dir, self.imgs[index]))
        
        image = Image.open(self.imgs[index])
        if self.transform:
            image = self.transform(image)

        return [image]


def run(imgs, processor):
    transform = transforms.Compose(
        [
            transforms.Grayscale(),
            transforms.ToTensor()
        ]
    )

    input_images = LunarSurfaceImageLoader(imgs=imgs, transform=transform)
    imageloader = DataLoader(input_images, batch_size=1, shuffle=False, collate_fn=lambda batch: list(zip(*batch)))

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)

    num_classes = 2
    # number of inputs in the fast r-cnn part
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # modify the fast r-cnn part
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    device = torch.device(processor)
    model.load_state_dict(torch.load(os.path.join('model', 'fasterrcnn_boulder_detector_35_3202.pt'), map_location=device))


    model = model.to(device)

    outputs = {}
    bboxes = {}

    cpu_device = torch.device("cpu")
    imshow = False
    with torch.no_grad():
        for i, images in enumerate(imageloader):
            images = list(image[0].to(device) for image in images)

            # setting the model to testing mode
            model.eval()

            outputs = model(images)
            #outputs = [{k: v.to(device) for k, v in t.items()} for t in targets]

            sample_image = images[0].permute(1, 2, 0).cpu().data.numpy()
            sample_bbox = outputs[0]['boxes']
            
            bboxes[input_images.imgs[i]] = sample_bbox.cpu().data.tolist()

    return bboxes


if __name__ == '__main__':
    bboxes = detect()

    print(bboxes)         
# with open('model/output/bboxes.json', 'w') as outfile:
#     json.dump(bboxes, outfile, sort_keys=True, indent=4)

# with open('bboxes.json', 'r') as f:
#     bboxes = json.load(f)

# for k,v in bboxes.items():
#     image = cv2.imread(os.path.join('../input/lunar-surface-dataseteval', 'test_data_LRO/test_data_LRO', k))
#     for bbox in v:
#         xy_min = (int(bbox[:2][0]), int(bbox[:2][1]))
#         xy_max = (int(bbox[2:][0]), int(bbox[2:][1]))
#         cv2.rectangle(image, xy_min, xy_max, (0, 0, 255), thickness=1)
    
#     file_name = k.replace('.png', '')
#     cv2.imwrite("{}_predicted.png".format(file_name), image)
