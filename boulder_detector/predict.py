import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision import transforms

from PIL import Image

import os
import json
from torch.utils.data import DataLoader, Dataset

import matplotlib.pyplot as plt
import cv2

class LunarSurfaceImageLoader(Dataset):

    def __init__(self, root_dir, img_dir, transform):
        self.root_dir = root_dir
        self.img_dir = img_dir
        self.transform = transform

        self.imgs = sorted(list(os.listdir(os.path.join(self.root_dir, self.img_dir))))

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, index):
        image = Image.open(os.path.join(self.root_dir, self.img_dir, self.imgs[index]))

        if self.transform:
            image = self.transform(image)

        return [image]

transform = transforms.Compose(
    [
        transforms.Grayscale(),
        transforms.ToTensor()
    ]
)

input_images = LunarSurfaceImageLoader(root_dir='data', img_dir='test_data_PANGU', transform=transform)
imageloader = DataLoader(input_images, batch_size=4, shuffle=False, collate_fn=lambda x: list(zip(*x)))

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)

num_classes = 2
# number of inputs in the fast r-cnn part
in_features = model.roi_heads.box_predictor.cls_score.in_features

# modify the fast r-cnn part
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

device = torch.device('cpu')
model.load_state_dict(torch.load(os.path.join("model", "fasterrcnn_boulder_detector.pt"), map_location=device))


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
        
        if imshow:
            if i % len(images) == 0:
                fig, ax = plt.subplots(1)
                plt.rcParams['figure.figsize'] = [40, 40]
                for bbox in sample_bbox:
                    xy_min = tuple(bbox[:2])
                    xy_max = tuple(bbox[2:])
                    cv2.rectangle(sample_image, xy_min, xy_max, (0, 0, 255), thickness=1)

                ax.imshow(sample_image)

                
with open('model/output/bboxes.json', 'w') as outfile:
    json.dump(bboxes, outfile, sort_keys=True, indent=4)