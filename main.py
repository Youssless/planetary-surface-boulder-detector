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

import util.conversions as c
import numpy as np

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

#model.load_state_dict(torch.load(os.path.join("model", "fasterrcnn_boulder_detector.pt")))

device = torch.device('cuda')
model = model.to(device)

outputs = {}
bboxes = {}

cpu_device = torch.device("cpu")
imshow = False

def output_bboxes():
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

    with open('bboxes.json', 'w') as outfile:
        json.dump(bboxes, outfile, sort_keys=True, indent=4)


def load_bounding_boxes():
    #bboxes = {}
    with open("data/bboxes.json", "r") as infile:
        bboxes = json.load(infile)

    return bboxes

def plot_bounding_boxes(num_plots):
    bboxes = load_bounding_boxes()
    for i, (k, v) in enumerate(bboxes.items()):
        if i == num_plots:
            break

        image = cv2.imread(os.path.join('data/test_data_PANGU', k))
        for bboxes in v:
            xy_min = (int(bboxes[:2][0]), int(bboxes[:2][1]))
            xy_max = (int(bboxes[2:][0]), int(bboxes[2:][1]))
            cv2.rectangle(image, xy_min, xy_max, (0, 0, 255), thickness=1)
            
        #fig, ax = plt.subplots(1)
        #ax.imshow(image)
        #plt.show()
        cv2.imwrite("data/test_data_PANGU/outputs/{}.png".format(i), image)

def get_cam_pos(fli_file):
    cam_pos = []
    with open(os.path.join("fli", fli_file)) as f:
        for line in f.readlines():
            line = line.split()
            cam_pos.append([int(line[1]), int(line[2])])

    return cam_pos


def to_PANGU_coordinates():
    bboxes = load_bounding_boxes()
    cam_pos = get_cam_pos("flight2.fli")
    center_points = []

    for i, (k, v) in enumerate(bboxes.items()):
        cp = []
        for j, bbox in enumerate(v):
            center = [abs((bbox[2]-bbox[0])/2), abs((bbox[3]-bbox[1])/2)]
            y_shift = 512-v[j][1]

            IMAGE_center_point = np.array([v[j][0]+center[0], y_shift-center[1]])
            PANGU_center_point = cam_pos[i] + ((IMAGE_center_point-250)*c.meters_per_pixel(350))

            if (-1024 <= PANGU_center_point[0] <= 1024) and (-512 <= PANGU_center_point[1] <= 512):
                cp.append(PANGU_center_point.tolist())

        center_points.append(cp)

    return center_points
    

def generate_boulderlist(file):
    center_points = to_PANGU_coordinates()
    # write to boulder list to use as input for PANGU
    write_list = []
    with open(file, "w") as f:
        for boulder_points in center_points:
            for point in boulder_points:
                write_list.append("{0} {1}".format(point[0], point[1]))
        
        f.write("\n".join(write_list))

if __name__ == '__main__':
    #plot_bounding_boxes(len(input_images))
    generate_boulderlist("boulder_list.txt")

