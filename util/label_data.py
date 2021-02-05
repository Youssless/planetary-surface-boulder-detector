import json
import math
import cv2 as cv
import numpy as np

from os import walk

far_dist = 3000
DEM_X = 1024
DEM_Y = 512


i = 0

coords = {}

# #coord_ranges = []
# for i in range(400):
#     camera_p = 0
#     with open("../fli/flight1.fli", "r") as f:
#         line = f.readline().split()[1:5]

        
#         near_dist = int(line[3]) # camera height

#         ratio = far_dist / near_dist
#         ratio_x = DEM_X / ratio
#         ratio_y = DEM_Y / ratio

#         camera_p = list(map(int, line[:2])) # camera point

#     with open("../../PANGU/PANGU_5.00/models/lunar_surface/boulder_list.txt", "r") as b_list:
#         lines = b_list.readlines()[6:] # from line 6 in the boulder list file

#         # for each line in the boulder list
#         for b_info in lines:
#             b_coords = list(map(float, b_info.split()[:2]))
            
#             #coord_ranges.append([-ratio_x,])
#             # if in the ratio range of the image
#             if -(ratio_x) <= b_coords[0] <= (ratio_x):
#                 if -(ratio_y) - i <= b_coords[1] <= (ratio_y) - i:
                    
#                     # check if the key, value pair is empty or not
#                     if i in coords:
#                         coords[i].append(b_coords)
#                     else:
#                         coords[i] = [b_coords]
#                     # add to dictionary


camera_pos = []
with open("../fli/flight1.fli", "r") as f:
    for line in f.readlines():
        camera_pos.append(line.split()[1:4])


def y_shift_coeff(img_h) -> float:
    return (1/512)*(512/0.366)

def y_shift(img_h):
    y_shifts = []
    for i in range(400):
        y_shifts.append(512 - abs(y_shift_coeff(img_h)*float(camera_pos[i][1])))

    return y_shifts


# with open("sample.json", "w") as outfile:  
#     json.dump(coords, outfile) 

"""
TODO
    - read json file 
        - for each image in the json file
            - create a csv file with the image name and the pixel coordinates for each boulder
"""

FOV = 30
IMAGE_DIM = 512

def meters_per_pixel(cam_h) -> float:
    ratio = 2*cam_h*math.tan(math.radians(FOV/2))

    return ratio / IMAGE_DIM

def to_pixel_coords():
    mpp = meters_per_pixel(350)
    coords = []
    pixel_coord = []
    pixel_coords = {}

    y_shifts = y_shift(IMAGE_DIM)
    with open("sample.json", "r") as read_file:
        data = json.load(read_file)
        
        for i, (k,v) in enumerate(data.items()):
            coords.append(v)
            for coords in v:
                
                x = (IMAGE_DIM/2) + (float(coords[0])/mpp)
                y = (IMAGE_DIM/2) + (float(coords[1])/mpp)
                
                y = y_shifts[i] - y
                pixel_coord.append([x, y])
                
            pixel_coords[i] = pixel_coord
            pixel_coord = []

    with open("pixel_coords.json", "w") as write_file:
        json.dump(pixel_coords, write_file)
               
    return pixel_coords



if __name__ == "__main__":
    px_coords = to_pixel_coords()

    _, _, filenames = next(walk("../frames"))

    #image = cv.imread('../frames/frame_00000.png')

    for i, (k, v) in enumerate(px_coords.items()):
        image = cv.imread('../frames/{0}'.format(filenames[int(k)]))
        for points in v:
            cv.drawMarker(image, (int(points[0]), int(points[1])), (0, 0, 255),
                 markerType=cv.MARKER_SQUARE, markerSize=1, thickness=2)
        
        cv.imwrite("../truths/{0}".format(filenames[int(k)]), image)

    # boulders = [
    #     [97.377018071711, -414.80678413063],
    #     [63.532890286297, -458.619938232],
    #     [-80.772529356182, -409.36112124473],
    #     [-4.3816952966154, -453.06013617665],
    #     [10.490165557712, -373.05140681565],
    #     [31.805287115276, -376.29753071815],
    #     [97.15769207105, -378.86919500306],
    #     [-58.256218209863, -432.81263904646]
    # ]

    # boulders_pix = []

    # for boulder in boulders:
    #     boulder_x = (IMAGE_DIM/2) + (boulder[0]/meters_per_pixel(350)) 
    #     boulder_y = (IMAGE_DIM/2) + (boulder[1]/meters_per_pixel(350))

    #     boulders_pix.append([boulder_x, boulder_y])
    # print(boulders_pix)

    # image = cv.imread('../frames/frame_00399.png')

    # for boulder in boulders_pix:
    #     cv.drawMarker(image, (int(boulder[0]), -578-int(boulder[1])), (0, 0, 255),
    #         markerType=cv.MARKER_SQUARE, markerSize=1, thickness=2)
    # # image = cv.circle(image, (int(boulders_pix[0][0]),512-int(boulders_pix[0][1])), radius=0, color=(0, 0, 255), thickness=2)
    # cv.imshow("Image", image)

    # cv.waitKey(0)

