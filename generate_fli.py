import numpy as np
import math
import util.conversions as c
import os
import copy

# q0 = np.array([0, 1, 0, 0], dtype="float") # initial quaternion
# q1 = np.array([0, 0.999998, 0, -0.00174533], dtype="float") # yaw quaternion
CAM_HEIGHT = 350
CAM_ROTATION = 180
CAM_TILT = 90
SURFACE_X = 1024
SURFACE_Y = 512
IMG_DIM = 512

mode = "test"
celestial_coords = np.array([CAM_HEIGHT, CAM_ROTATION, CAM_TILT]) # range(m), azimuth, altitude

# taking images of the whole lunar surface to use for testing against real boulder points
if mode == "test":
    axis_length = math.floor(c.meters_per_pixel(CAM_HEIGHT)*IMG_DIM)
    x_center = math.floor(SURFACE_X - axis_length/2)
    y_center = math.floor(SURFACE_Y - axis_length/2)

    cam_center_point = np.array([x_center, y_center, 0])

    T_FACTOR = np.array([-axis_length, 0, 0])

    num_cols = math.floor((SURFACE_X*2)/axis_length)
    num_rows = math.ceil((SURFACE_Y*2)/axis_length)

    i = j = 0
    while j < num_rows:
        with open(os.path.join("fli", "flight1.fli"), "a") as f:
            f.write(
                "start\t" + str(cam_center_point[0]) + " " + str(cam_center_point[1]) + " " + str(cam_center_point[2]) + "\t" 
                + str(celestial_coords[0]) + " " + str(celestial_coords[1]) + " " + str(celestial_coords[2]) + "\n"
                )
        
        if i < num_cols:
            cam_center_point += T_FACTOR
            i += 1
        else:
            cam_center_point += np.array([0, -(axis_length), 0])
            T_FACTOR *= -1
            i = 0
            j += 1
# generate training images
elif mode == "train":
    x_center = y_center = 0
    cam_center_point = np.array([x_center, y_center])
    T_FACTOR = np.array([
                        [0.0, -1.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [-1.0, 0.0, 0.0],
                        [1.0, 0.0, 0.0]
                    ])

    j = 0
    for i in range(1600):
        with open("fli/flight1.fli", "a") as f:
            f.write(
                "start\t" + str(cam_center_point[0]) + " " + str(cam_center_point[1]) + " " + str(cam_center_point[2]) + "\t" 
                + str(celestial_coords[0]) + " " + str(celestial_coords[1]) + " " + str(celestial_coords[2]) + "\n"
                )

        if i != 0 and i % 400 == 0:
            cam_coords = np.array([0, 0, 0])
            j += 1
        
        cam_coords = cam_coords + T_FACTOR[j]