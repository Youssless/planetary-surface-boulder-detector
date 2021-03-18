import cv2
import numpy as np
import os
import json

from util import utils

import math

SIZE_X = 1024
SIZE_Y = 512
CAM_H = 350
IMG_SIZE = 512

BBOXES = 'data/bboxes.json'
IMAGE_DIR = 'data/test_data_PANGU'
FLI_FILE = 'fli/flight2.fli'

TARGET_DIR = "../PANGU/PANGU_5.00/models"

targets = ["{0}/lunar_surface_predicted/feature_lists/boulder".format(TARGET_DIR)
            ,"{0}/lunar_surface_m185903952re/feature_lists/boulder".format(TARGET_DIR)]

TARGET = targets[0]
BL_FILE_NAME = "boulder_list_ls_predicted.txt"

def batch_load_bounding_boxes():
    #bboxes = {}
    with open(BBOXES, "r") as infile:
        b = json.load(infile)

    return b

def load_bounding_boxes(img_name):
    with open(BBOXES, "r") as infile:
        b = json.load(infile)

        boxes = {}
        for im in b:
            if im == img_name:
                boxes[im] = b[im] 
  
    return boxes


is_PANGU_image = True
bboxes = {}

if is_PANGU_image:
    cam_pos = utils.get_camera_positions(fli_file=FLI_FILE)
    cam_pos = np.delete(cam_pos, 2, axis=1) # delete the last column (z coordinate not needed)
    bboxes = batch_load_bounding_boxes()
    IMG_WIDTH = IMG_SIZE / utils.pixels_per_meter(CAM_H)
else:
    cam_pos = np.array([[0, 0]])
    bboxes = load_bounding_boxes('M185903952RE_thumb.png')
    IMG_WIDTH = 852
        




# def plot_bounding_boxes(num_plots):

#     for i, (k, v) in enumerate(bboxes.items()):
#         if i == num_plots:
#             break

#         image = cv2.imread(os.path.join(IMAGE_DIR, k))
#         for bboxes in v:
#             xy_min = (int(bboxes[:2][0]), int(bboxes[:2][1]))
#             xy_max = (int(bboxes[2:][0]), int(bboxes[2:][1]))
#             cv2.rectangle(image, xy_min, xy_max, (0, 0, 255), thickness=1)
            
#         #fig, ax = plt.subplots(1)
#         #ax.imshow(image)
#         #plt.show()
#         cv2.imwrite("{0}/outputs/{1}.png".format(IMAGE_DIR,i), image)


def _generate_boulderlist():
    # list of boulder center points
    boulder_list = []
    scale = utils.meters_per_pixel(CAM_H) if is_PANGU_image else IMG_SIZE / IMG_WIDTH

    for i, (k, v) in enumerate(bboxes.items()):
        cp = []
        for bbox in v:
            diameter = np.array([abs((bbox[2]-bbox[0])), abs((bbox[3]-bbox[1]))])
            radius = np.array([abs((bbox[2]-bbox[0])/2), abs((bbox[3]-bbox[1])/2)])

            # flip the y axis to to align with the PANGU coordinate system before conversion
            y_shift = IMG_SIZE-bbox[1]

            # center point of the bounding box
            bbox_center_point = np.array([bbox[0]+radius[0], y_shift-radius[1]])

            # center point of the boulder in PANGU
            boulder_center_point = cam_pos[i] + ((bbox_center_point-IMG_SIZE*0.5)*utils.meters_per_pixel(CAM_H)) if is_PANGU_image \
                else cam_pos[i] + ((bbox_center_point-IMG_SIZE*0.5))

            # make sure the boulder coordinates are within the surface range
            if (-SIZE_X <= boulder_center_point[0] <= SIZE_X) and (-SIZE_Y <= boulder_center_point[1] <= SIZE_Y):

                # size of the boulder is the diameter, PANGU will use this diameter to calculate the area
                boulder_size = diameter[0]*scale if diameter[0] < diameter[1] else diameter[1]*scale

                # elevation based of the boulder size
                elevation = boulder_size*0.5 if boulder_size <= 2 else boulder_size*0.1

                # library num always 1
                library_num = 1

                cp.append([*boulder_center_point.tolist(), boulder_size, elevation, library_num])

        boulder_list.append(cp)

    return boulder_list 

def generate_boulderlist(file):
    boulders = _generate_boulderlist()
    # write to boulder list to use as input for PANGU
    write_list = []
    write_list.append(
    """identifier PANGU: Boulder List File
horizontal_scale 1
offset 0 0
size {0} {1}""".format(2000, 2000)
    )
    with open(os.path.join(TARGET, file), "w") as f:
        for boulder in boulders:
            for attrib in boulder:
                write_list.append("{0} {1} {2} {3} {4}".format(attrib[0], attrib[1], attrib[2], attrib[3], attrib[4]))
        
        f.write("\n".join(write_list))


if __name__ == '__main__':
    #plot_bounding_boxes(8)
    generate_boulderlist(BL_FILE_NAME)
