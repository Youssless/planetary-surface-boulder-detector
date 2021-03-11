import cv2
import numpy as np
import os
import json

from util import utils

import math

SIZE_X = 1024
SIZE_Y = 512

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



def _generate_boulderlist():
    bboxes = load_bounding_boxes()

    cam_pos = utils.get_camera_positions(fli_file="fli/flight2.fli")
    cam_pos = np.delete(cam_pos, 2, axis=1) # delete the last column (z coordinate not needed)
    
    # list of boulder center points
    boulder_list = []

    for i, (k, v) in enumerate(bboxes.items()):
        cp = []
        for bbox in v:
            # x, y radius of the bouding box
            radius = np.array([abs((bbox[2]-bbox[0])/2), abs((bbox[3]-bbox[1])/2)])
            m_radius = radius*utils.meters_per_pixel(350)
            # flip the y axis to to align with the PANGU coordinate system before conversion
            y_shift = 512-bbox[1]

            # center point of the bounding box
            bbox_center_point = np.array([bbox[0]+radius[0], y_shift-radius[1]])

            # center point of the boulder in PANGU
            boulder_center_point = cam_pos[i] + ((bbox_center_point-250)*utils.meters_per_pixel(350))

            # make sure the boulder coordinates are within the surface range
            if (-SIZE_X <= boulder_center_point[0] <= SIZE_X) and (-SIZE_Y <= boulder_center_point[1] <= SIZE_Y):
                # area_of_oval = a*b*pi
                # boulder_size (in PANGU) = area_of_oval*meters_per_pixel
                boulder_size = m_radius[0]*m_radius[1]*math.pi

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
    with open(os.path.join("data/boulders/boulder_lists", file), "w") as f:
        for boulder in boulders:
            for attrib in boulder:
                write_list.append("{0} {1} {2} {3} {4}".format(attrib[0], attrib[1], attrib[2], attrib[3], attrib[4]))
        
        f.write("\n".join(write_list))

if __name__ == '__main__':
    #plot_bounding_boxes(len(input_images))
    generate_boulderlist("boulder_list.txt")

