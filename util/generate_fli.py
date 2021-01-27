import numpy as np

q0 = np.array([0, 1, 0, 0], dtype="float") # initial quaternion
q1 = np.array([0, 0.999998, 0, -0.00174533], dtype="float") # yaw quaternion

cam_coords = np.array([0, 0, 0])
celestial_coords = np.array([350, 90, 90]) # range(m), azimuth, altitude
T_FACTOR = np.array([0.0, -1.0, 0.0], dtype="float")


for i in range(400):
    with open("../flight_files/flight1.fli", "a") as f:
        f.write(
            "start\t" + str(cam_coords[0]) + " " + str(cam_coords[1]) + " " + str(cam_coords[2]) + "\t" 
            + str(celestial_coords[0]) + " " + str(celestial_coords[1]) + " " + str(celestial_coords[2]) + "\n"
            )

    #q0[1] *= q1[1]
    cam_coords = cam_coords + T_FACTOR
    #q0[3] += q1[3]