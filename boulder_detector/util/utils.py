import math
import numpy as np
import os

far_dist = 3000
DEM_X = 1024
DEM_Y = 512
FOV = 30
IMAGE_DIM = 512
NUM_IMAGES = 400

def get_boulder_info(boulder_list):
    boulder_info = []
    with open(boulder_list) as f:
        for i, line in enumerate(f.readlines()):
            # skip the first 5 lines
            if i < 6:
                continue
            boulder_info.append(line.split())

    return np.array(boulder_info, dtype="float")

def get_camera_positions(fli_file):
    camera_pos = []
    with open(fli_file, "r") as f:
        for line in f.readlines():
            camera_pos.append(line.split()[1:4])

    return np.array(camera_pos, dtype='float')


def pixels_per_meter(cam_h) -> float:
    '''Number of pixels per meter the camera travelles

    Args:
        cam_h (int): Camera height in meters that was used to take the image

    Returns:
        float: returns the number of pixels per meter
    '''
    return (1/IMAGE_DIM)*(IMAGE_DIM/meters_per_pixel(cam_h))


def y_shift(cam_h, fli_file) -> list:
    '''Shift the y coordinate to fit opencv coordinate axis

    Args:
        cam_h (int): Camera height in meters that was used to take the image

    Returns:
        list (float): returns the value to shift each boulder in each image in the y-axis
    '''
    y_shifts = []
    camera_pos = get_camera_positions(fli_file=fli_file)
    for i in range(len(camera_pos)):
        # shift the y depending on the camera position
        y_shifts.append(512 - abs(float(camera_pos[i][1])/meters_per_pixel(cam_h)))

    return y_shifts


def meters_per_pixel(cam_h) -> float:
    '''Calculate the meters by pixel ratio

    Args:
        cam_h (int): Camera height in meters that was used to take the image

    Returns:
        float: returns the meter per pixel ratio
    '''

    ratio = 2*cam_h*math.tan(math.radians(FOV/2))-3

    return ratio / IMAGE_DIM

def boulder_elevation(size):
    return 1/(1 + np.exp(-size)) - 0.5