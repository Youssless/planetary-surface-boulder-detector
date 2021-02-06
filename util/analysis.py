import matplotlib.pyplot as plt
import numpy as np
import math

import cv2

cam_coords = []
with open("../fli/flight1.fli", "r") as f:
    for cam_coord in f.readlines():
        cam_coords.append(float(cam_coord.split()[2:3][0]))

def y_shift_coeff(img_h) -> float:
    return (1/512)*(512/0.366)

def y_shift(img_h):
    y_shifts = []
    for i in range(400):
        y_shifts.append(512 - abs(y_shift_coeff(img_h)*cam_coords[i]))

    return y_shifts


def run_analysis():
    cam_coords = np.array(cam_coords)
    y_shifts = np.array(y_shift(512))

    #print(y_shifts)

    fig = plt.figure()
    ax = plt.axes()

    ax.plot(cam_coords, y_shifts)
    plt.show()


data = [[201.5483335343505, 217.65367308237143],
        [306.3882295496668, 351.17129278503796],
        [448.2536427499957, 439.9697997487798],
        [414.90455583820926, 504.912956366436],
        [454.1508280555321, 246.95873321692807],
        [237.72091049635327, 102.45122769140028],
        [282.6764951634275, 401.8101037939715],
        [400.84039385411023, 31.31041631184337],
        [136.7745459486532, 413.56446689311804],
        [327.2703317907032, 81.63784140916681],
        [358.2835642167374, 61.09003972095513],
        [473.659502181912, 132.75926956555134]]

image = cv2.imread('../frames/frame_00000.png')

data = np.array(data)
data = np.floor(data)
data = data.astype(int)
#print(tuple(int(data[0])))

data = map(tuple, data)
data = tuple(data)
print(data)

for i in range(12):
    cv2.rectangle(image, (data[i][0]-5, data[i][1]-5), (data[i][0]+5, data[i][1]+5), (0, 0, 255), 1)
cv2.imshow("Image", image)
cv2.waitKey(0)