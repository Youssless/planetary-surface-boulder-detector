import json

far_dist = 3000
DEM_X = 1024
DEM_Y = 512


i = 0

coords = {}
for i in range(400):
    camera_p = 0
    with open("../fli/flight1.fli", "r") as f:
        line = f.readline().split()[1:5] 
        
        near_dist = int(line[3]) # camera height

        ratio = far_dist / near_dist
        ratio_x = DEM_X / ratio
        ratio_y = DEM_Y / ratio

        camera_p = list(map(int, line[:2])) # camera point

    with open("../../PANGU/PANGU_5.00/models/lunar_surface/boulder_list.txt", "r") as b_list:
        lines = b_list.readlines()[6:] # from line 6 in the boulder list file

        # for each line in the boulder list
        for b_info in lines:
            b_coords = list(map(float, b_info.split()[:2]))
            
            # if in the ratio range of the image
            if -(ratio_x) <= b_coords[0] <= (ratio_x):
                if -(ratio_y) - i <= b_coords[1] <= (ratio_y) - i:
                    
                    # check if the key, value pair is empty or not
                    if i in coords:
                        coords[i].append(b_coords)
                    else:
                        coords[i] = [b_coords]
                    # add to dictionary


with open("sample.json", "w") as outfile:  
    json.dump(coords, outfile) 