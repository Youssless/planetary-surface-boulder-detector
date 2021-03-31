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
from util import utils 

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


def _generate_boulderlist(bboxes, **kwargs):
    has_camera = bool(kwargs['has_camera'])
    image_size = kwargs['image_size']
    terrain_size = [kwargs['surface_x'], kwargs['surface_z']]

    if has_camera:
        cam_h = kwargs['cam_h']
        cam_pos = utils.get_camera_positions(fli_file=kwargs['fli_file'])
        actual_img_width = image_size[0] / utils.pixels_per_meter(cam_h)
        scale = utils.meters_per_pixel(cam_h)
    else:
        cam_h = 0
        cam_pos = np.array([[0, 0]])
        actual_img_width = kwargs['actual_img_width']
        scale = 1 # image_size / actual_img_width
    
    # list of boulder center points
    boulder_list = []

    for i, (k, v) in enumerate(bboxes.items()):
        cp = []
        for bbox in v:
            diameter = np.array([abs((bbox[2]-bbox[0])), abs((bbox[3]-bbox[1]))])
            radius = np.array([abs((bbox[2]-bbox[0])/2), abs((bbox[3]-bbox[1])/2)])

            # flip the y axis to to align with the PANGU coordinate system before conversion
            y_shift = image_size-bbox[1]

            # center point of the bounding box
            bbox_center_point = np.array([bbox[0]+radius[0], y_shift-radius[1]])

            # center point of the boulder in PANGU
            boulder_center_point = cam_pos[i] + ((bbox_center_point-image_size*0.5)*utils.meters_per_pixel(cam_h)) if has_camera \
                else cam_pos[i] + ((bbox_center_point-image_size*0.5))

            # make sure the boulder coordinates are within the surface range
            if (-terrain_size[0] <= boulder_center_point[0] <= terrain_size[0]) and (-terrain_size[1] <= boulder_center_point[1] <= terrain_size[1]):

                # size of the boulder is the diameter, PANGU will use this diameter to calculate the area
                boulder_size = diameter[0]*scale if diameter[0] < diameter[1] else diameter[1]*scale

                # elevation based of the boulder size
                elevation = utils.boulder_elevation(boulder_size)

                # library num always 1
                library_num = 1

                cp.append([*boulder_center_point.tolist(), boulder_size, elevation, library_num])

        boulder_list.append(cp)

    return boulder_list

def _predict(processor, imgs):
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
    model.load_state_dict(torch.load(os.path.join(os.path.dirname(__file__), 'model', 'fasterrcnn_boulder_detector_35_3202.pt'), map_location=device))


    model = model.to(device)

    outputs = {}
    bboxes = {}

    cpu_device = torch.device("cpu")
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

def run(**kwargs):
    
    bboxes = _predict(kwargs['processor'], kwargs['imgs'])
    boulderlist = _generate_boulderlist(bboxes, **kwargs)
    
    #testing
    BL_FILE_NAME = "boulder_list_m185903952re.txt"
    generate_boulderlist(BL_FILE_NAME, boulderlist)

    return boulderlist


def generate_boulderlist(file, boulders):
    #testing
    TARGET_DIR = "{}\\..\\..\\PANGU\\PANGU_5.00\\models".format(os.path.dirname(__file__))
    print(TARGET_DIR)

    targets = ["{0}/lunar_surface_predicted/feature_lists/boulder".format(TARGET_DIR)
                ,"{0}/lunar_surface_m185903952re/feature_lists/boulder/{1}".format(TARGET_DIR, file)]

    TARGET = targets[1]
    
    print(print(targets[1]))
    # write to boulder list to use as input for PANGU
    write_list = []
    write_list.append(
    """identifier PANGU: Boulder List File
horizontal_scale 1
offset 0 0
size {0} {1}""".format(1200, 1200)
    )
    with open(targets[1], "w+") as f:
        for boulder in boulders:
            for attrib in boulder:
                write_list.append("{0} {1} {2} {3} {4}".format(attrib[0], attrib[1], attrib[2], attrib[3], attrib[4]))
        
        f.write("\n".join(write_list))

# if __name__ == '__main__':
#     bboxes = detect()

#     print(bboxes)         
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
