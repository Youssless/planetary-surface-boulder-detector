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

data = np.array(data, dtype="uint32")
image = cv2.imread('../frames/frame_00000.png')

imhsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
ret, thresh = cv2.threshold(imhsv[:,:,0], 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

fin = cv2.bitwise_and(image, image, mask = thresh)



original = fin.copy()

gray = cv2.cvtColor(fin,cv2.COLOR_BGR2GRAY)

# threshold
thresh = cv2.threshold(gray,25,255,cv2.THRESH_BINARY)[1]
result = fin.copy()
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for cntr in contours:
    x,y,w,h = cv2.boundingRect(cntr)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
    print("x,y,w,h:",x,y,w,h)
 
# save resulting image
cv2.imwrite('two_blobs_result.jpg',result)      

# show thresh and result    
cv2.imshow("bounding_box", image)
cv2.waitKey(0)