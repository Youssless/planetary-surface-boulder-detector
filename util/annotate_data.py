import json
import math
import cv2 as cv
import numpy as np


from os import walk

far_dist = 3000
DEM_X = 1024
DEM_Y = 512
FOV = 30
IMAGE_DIM = 512
NUM_IMAGES = 400


class Camera:

    def __init__(self, fov, fli_file):
        self.fov = fov
        self.fli_file = fli_file

        self.height = self._get_height()

    def get_locations(self):
        camera_locs = []
        with open(self.fli_file) as f:
            for line in f.readlines():
                camera_locs.append(line.split()[1:4])

        return np.array(camera_locs, dtype='float')

    def _get_height(self):
        height = 0
        with open(self.fli_file) as f:
            line = f.readline()
            height = int(line.split()[4:5][0])

        return height

    def __str__(self):
        return "FOV: {0}\nHeight: {1}\nfli_file: {2}".format(fov, height, fli_file)


cam = Camera(fov=30, fli_file="../fli/flight1.fli")

def get_boulder_info():
    boulder_info = []
    with open("../../PANGU/PANGU_5.00/models/lunar_surface/boulder_list.txt") as f:
        for i, line in enumerate(f.readlines()):
            # skip the first 5 lines
            if i < 6:
                continue
            boulder_info.append(line.split())

    return np.array(boulder_info, dtype="float")


camera_pos = []
with open("../fli/flight1.fli", "r") as f:
    for line in f.readlines():
        camera_pos.append(line.split()[1:4])


def pixels_per_meter(cam_h) -> float:
    '''Number of pixels per meter the camera travelles

    Args:
        cam_h (int): Camera height in meters that was used to take the image

    Returns:
        float: returns the number of pixels per meter
    '''
    return (1/IMAGE_DIM)*(IMAGE_DIM/meters_per_pixel(cam_h))


def y_shift(cam_h) -> list:
    '''Shift the y coordinate to fit opencv coordinate axis

    Args:
        cam_h (int): Camera height in meters that was used to take the image

    Returns:
        list (float): returns the value to shift each boulder in each image in the y-axis
    '''
    y_shifts = []
    for i in range(400):
        # shift the y depending on the camera position
        y_shifts.append(512 - abs(pixels_per_meter(cam_h)*float(camera_pos[i][1])))

    return y_shifts


def meters_per_pixel(cam_h) -> float:
    '''Calculate the meters by pixel ratio

    Args:
        cam_h (int): Camera height in meters that was used to take the image

    Returns:
        float: returns the meter per pixel ratio
    '''

    ratio = 2*cam_h*math.tan(math.radians(FOV/2))

    return ratio / IMAGE_DIM

def search_boulders():
    i = 0
    coords = {}

    cam_locs = cam.get_locations()
    boulder_info = get_boulder_info()

    search_range = np.array([
                        [-(IMAGE_DIM * meters_per_pixel(cam.height))/2, (IMAGE_DIM * meters_per_pixel(cam.height))/2], # x
                        [-(IMAGE_DIM * meters_per_pixel(cam.height))/2, (IMAGE_DIM * meters_per_pixel(cam.height))/2]  # y
                    ], dtype="float")
    

    for i in range(400):
        for b in boulder_info:
            if search_range[0][0] <= b[0] <= search_range[0][1]: # x search
                if (search_range[1][0] + cam_locs[i][1]) <= b[1] <= (search_range[1][1] + cam_locs[i][1]): # y search
                    b_list= b.tolist()
                    if i in coords:
                        coords[i].append(b_list)
                    else:
                        coords[i] = [b_list]
    
    # write into a json file boulder_cppi.json (boulder camera points per image)
    with open("boulder_cppi.json", "w") as write_file:
        json.dump(coords, write_file)


def to_pixel_coords(cam_h) -> list:
    '''Calculate the pixel coordinates per boulder per image and store them in JSON format

        Args:
            cam_h (int): Camera height in meters that was used to take the image

        Returns:
            pixel_coords([float]): returns the pixel coordinate per boulder per image
    '''
    mpp = meters_per_pixel(350)
    coords = []
    pixel_coord = []
    pixel_coords = {}

    y_shifts = y_shift(cam_h)
    with open("boulder_cppi.json", "r") as read_file:
        data = json.load(read_file)
        
        for i, (k,v) in enumerate(data.items()):
            coords.append(v)
            for coords in v:
                
                x = (IMAGE_DIM/2) + (float(coords[0])/mpp)
                y = (IMAGE_DIM/2) + (float(coords[1])/mpp)

                size = math.trunc(float(coords[2])/mpp)
                
                y = y_shifts[i] - y
                pixel_coord.append([x-(size), y-(size), size])
                
            pixel_coords[i] = pixel_coord
            pixel_coord = []

    with open("pixel_coords.json", "w") as write_file:
        json.dump(pixel_coords, write_file)
               
    return pixel_coords

def annotate_images(cam_h):
    '''Annotate each boulder in each image with a red point

        Args:
            cam_h (int): Camera height in meters that was used to take the image
    '''
    # pixel coordinate list of all the boulders in each image
    px_coords = to_pixel_coords(cam_h) 
    _, _, filenames = next(walk("../frames"))

    # read, plot and write each image in the dataset
    for i, (k, v) in enumerate(px_coords.items()):
        image = cv.imread('../frames/{0}'.format(filenames[int(k)]))
        for points in v:
            start_point = (int(points[0]), int(points[1]))
            end_point = (int(points[0])+int(2*points[2]), int(points[1])+int(2*points[2]))
            cv.rectangle(image, start_point, # start point
                                end_point, # end point
                                (0, 0, 255), thickness=1)
        
        cv.imwrite("../truths/{0}".format(filenames[int(k)]), image)


if __name__ == "__main__":
    search_boulders()
    to_pixel_coords(cam.height)
    annotate_images(cam.height)

