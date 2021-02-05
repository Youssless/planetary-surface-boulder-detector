import matplotlib.pyplot as plt
import numpy as np

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


cam_coords = np.array(cam_coords)
y_shifts = np.array(y_shift(512))

#print(y_shifts)

fig = plt.figure()
ax = plt.axes()

ax.plot(cam_coords, y_shifts)
plt.show()