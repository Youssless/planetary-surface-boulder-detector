import json
import math
import cv2 as cv

far_dist = 3000
DEM_X = 1024
DEM_Y = 512


i = 0

coords = {}

# coord_ranges = []
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



def normalise_coord(value, min_v, max_v) -> float:
    """Normalise ethier x or y coordinates between 0 and 1. 
        
        This will give a percentage to map the actual boulder coordinate with
        the image boulder coordinate.

    Parameters
    ----------
    value: float
        Actual boulder coordinate in ethier x or y
    min_v: float
        Actual axis range. If value specified is an x coordinate then the min_v
            should be in the x axis and vice versa
    max_v: float
        Actual axis range. If value specified is an x coordinate then the min_v
            should be in the x axis and vice versa

    Returns
    -------
    float
        Percentage that maps to pixel coordinates of the image
    """
    return abs((value-min_v)/(max_v-min_v))


#print(to_image_coords())

def to_image_coords(normalised_coord, min_d, max_d) -> float:
    """Convert the boulder coordinate to pixel coordinate

    Parameters
    ----------
    normalised_coord: float
        Percentage used to multiply the actual boulder coord with the width of the image.
        Percentage is returned in normalised_coord(value, min_v, max_v)
    min_d: float
        Minimum coord for the destination. Axis needs to match normalised_coord percentage
    max_d: float
        Maximum coord for the destination. Axis needs to match normalised_coord percentage

    """
    return normalised_coord*(abs(max_d-min_d)) + min_d

# with open("sample.json", "w") as outfile:  
#     json.dump(coords, outfile) 

FOV = 30
IMAGE_DIM = 512

def meters_per_pixel(cam_h):
    ratio = 2*cam_h*math.tan(math.radians(FOV/2))

    return IMAGE_DIM / ratio

boulders = [
        [-19.947648514062, 14.047670178115],
        [18.459062092006, -34.864745568484],
        [72.589937597513, 3.3121486194432],
        [-6.696302909404, 56.250563822687],
        [9.7725815139711, -53.415604867041],
        [113.81692904979, -40.931636933237],
        [-43.676669709384, -57.721660472453],
        [79.736682586372, 45.147613156587],
        [101.56002314761, -50.523466430604]
]

boulders_pix = []

for boulder in boulders:
    boulder_x = (IMAGE_DIM/2) + (boulder[0]*meters_per_pixel(350))
    boulder_y = (IMAGE_DIM/2) + (boulder[1]*meters_per_pixel(350))

    boulders_pix.append([boulder_x, boulder_y])
print(boulders_pix)

image = cv.imread('../frames/scr_00000.png')

for boulder in boulders_pix:
    cv.drawMarker(image, (int(boulder[0]), 512-int(boulder[1])), (0, 0, 255),
        markerType=cv.MARKER_SQUARE, markerSize=1, thickness=2)
# image = cv.circle(image, (int(boulders_pix[0][0]),512-int(boulders_pix[0][1])), radius=0, color=(0, 0, 255), thickness=2)
cv.imshow("Image", image)

cv.waitKey(0)

