import requests

BASE = "http://127.0.0.1:5000/predict"
result = requests.get(BASE + "/D:%2fWorkspace%2funiversity%2fYR4%2fhons_proj%2fplanetary-surface-boulder-detector%2fboulder_detector%2fdata%2ftest_data_LRO%2fM111545012RE.crop.png/cpu")
print(result.json())