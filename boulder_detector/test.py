import requests

BASE = "http://127.0.0.1:5000/predict?"
PROCESSOR = "cpu"
IMGS = "D:%2fWorkspace%2funiversity%2fYR4%2fhons_proj%2fplanetary-surface-boulder-detector%2fboulder_detector%2fdata%2ftest_data_LRO%2fM185903952RE_thumb.png"
IMAGE_SIZE = "1200"
ACTUAL_IMG_WIDTH = "832"
SURFACE_X = "1200"
SURFACE_Z = "1200"
HAS_CAMERA = "False"
CAM_H = "0"
FLI_FILE = "None"


query = BASE + \
"processor=" + PROCESSOR + "&" + \
"imgs=" + IMGS + "&" + \
"image_size=" + IMAGE_SIZE + "&" + \
"actual_img_width=" + ACTUAL_IMG_WIDTH + "&" + \
"surface_x=" + SURFACE_X + "&" + \
"surface_z=" + SURFACE_Z + "&" + \
"has_camera=" + HAS_CAMERA + "&" + \
"cam_h=" + CAM_H + "&" + \
"fli_file=" + FLI_FILE

result = requests.get(query)
print(result.json())