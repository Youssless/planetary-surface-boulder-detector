import json
import math
import cv2 as cv
import numpy as np

import os
from os import walk

from util import utils

far_dist = 3000
DEM_X = 1024
DEM_Y = 512
FOV = 30
IMAGE_DIM = 512
NUM_IMAGES = 400

CPPI_FILE_NAME = "boulder_cppi.json"
PPPI_FILE_NAME = "boulder_pppi.json"


def search_boulders():
    i = 0
    coords = {}

    cam_locs = utils.get_camera_positions(fli_file="fli/flight2.fli")
    boulder_info = utils.get_boulder_info(boulder_list="../PANGU/PANGU_5.00/models/lunar_surface/boulder_list.txt")

    search_range = np.array([
                        [-(IMAGE_DIM * utils.meters_per_pixel(350))/2, (IMAGE_DIM * utils.meters_per_pixel(350))/2], # x
                        [-(IMAGE_DIM * utils.meters_per_pixel(350))/2, (IMAGE_DIM * utils.meters_per_pixel(350))/2]  # y
                    ], dtype="float")
    

    for i in range(len(cam_locs)):
        for b in boulder_info:
            if search_range[0][0] <= b[0] <= search_range[0][1]: # x search
                if (search_range[1][0] + cam_locs[i][1]) <= b[1] <= (search_range[1][1] + cam_locs[i][1]): # y search
                    b_list= b.tolist()
                    if i in coords:
                        coords[i].append(b_list)
                    else:
                        coords[i] = [b_list]
    
    # write into a json file boulder_cppi.json (boulder camera points per image)
    with open(os.path.join("data/boulders/boulder_points", CPPI_FILE_NAME), "w") as write_file:
        json.dump(coords, write_file)


def to_pixel_coords() -> list:
    '''Calculate the pixel coordinates per boulder per image and store them in JSON format

        Args:
            cam_h (int): Camera height in meters that was used to take the image

        Returns:
            pixel_coords([float]): returns the pixel coordinate per boulder per image
    '''
    # mpp = meters per pixel constant 
    mpp = utils.meters_per_pixel(350)
    coords = []
    pixel_coord = []
    pixel_coords = {}

    y_shifts = utils.y_shift(350, fli_file='fli/flight2.fli')
    with open(os.path.join("data/boulders/boulder_points", CPPI_FILE_NAME), "r") as read_file:
        data = json.load(read_file)
        
        for i, (k,v) in enumerate(data.items()):
            coords.append(v)
            for coords in v:
                
                # center of the image + pixel coordinate of the boulder
                x = (IMAGE_DIM/2) + (float(coords[0])/mpp)
                y = (IMAGE_DIM/2) + (float(coords[1])/mpp)

                # size of boulders in pixel coordinates
                size = float(coords[2])/mpp
                
                # shift the y to fit the coordinate system of opencv
                y = y_shifts[i] - y

                pixel_coord.append([x-(size/2), y-(size/2), size])
  
            pixel_coords[i] = pixel_coord
            pixel_coord = []
    
    # boulder pixel points per image
    with open(os.path.join("data/boulders/boulder_points", PPPI_FILE_NAME), "w") as write_file:
        json.dump(pixel_coords, write_file)
               
    return pixel_coords

def annotate_images():
    '''Annotate each boulder in each image with a red point

        Args:
            cam_h (int): Camera height in meters that was used to take the image
    '''
    # pixel coordinate list of all the boulders in each image
    px_coords = to_pixel_coords(350) 
    _, _, filenames = next(walk("../frames"))

    # read, plot and write each image in the dataset
    for i, (k, v) in enumerate(px_coords.items()):
        image = cv.imread('../frames/{0}'.format(filenames[int(k)]))
        for points in v:
            start_point = (int(math.ceil(points[0])), int(math.ceil(points[1])))
            end_point = (int(math.ceil(points[0] + (points[2]))), int(math.ceil(points[1]+(points[2]))))
            cv.rectangle(image, start_point, # start point
                                end_point, # end point
                                (0, 0, 255), thickness=1)
        
        cv.imwrite("../truths/{0}".format(filenames[int(k)]), image)



if __name__ == "__main__":
    search_boulders()
    to_pixel_coords()

    annotate = False
    if annotate:
        annotate_images()

