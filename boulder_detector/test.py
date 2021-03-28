import requests

BASE = "http://127.0.0.1:5000/predict"
PROCESSOR = "/cpu"
IMGS = "/D:%2fWorkspace%2funiversity%2fYR4%2fhons_proj%2fplanetary-surface-boulder-detector%2fboulder_detector%2fdata%2ftest_data_LRO%2fM111545012RE.crop.png"
IMAGE_SIZE = "/1200"
ACTUAL_IMG_WIDTH = "/832"
SURFACE_X = "/1200"
SURFACE_Z = "/1200"
HAS_CAMERA = "/0"
CAM_H = "/0"
FLI_FILE = "/None"


query = BASE + \
PROCESSOR + \
IMGS + \
IMAGE_SIZE + \
ACTUAL_IMG_WIDTH + \
SURFACE_X  + \
SURFACE_Z + \
HAS_CAMERA + \
CAM_H + \
FLI_FILE

result = requests.get(query)
print(result.json())