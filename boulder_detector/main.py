from flask import Flask, request
from flask_restful import Api, Resource
import predict
import requests

app = Flask(__name__)
api = Api(app)

class BoulderDetector(Resource):
    def get(self, processor, imgs, 
            image_size, actual_img_width, 
            surface_x, surface_z, has_camera, 
            cam_h, fli_file):
        # need to import predict.py
        # call method to predict a single image
        # return json of predicted bounding boxes
        result = predict.run(
            processor=processor,
            imgs=imgs,
            image_size=image_size,
            actual_img_width=actual_img_width,
            surface_x=surface_x,
            surface_z=surface_z,
            has_camera=has_camera,
            cam_h=cam_h,
            fli_file=fli_file,
        )

        # arguments needed:
        '''
        - image
        - processor {cpu, gpu}
        - image_size
        - camera_height (optional - PANGU)
        - fli_file (optional - PANGU)
        - boulder_list_file_name
        - output_folder
        - scale
        '''
        
        return {"data": result}

class MakeBoulderList(Resource):
    def get(self):
        pass

# api endpoint for getting the predicted bounding boxes
api.add_resource(BoulderDetector, '/predict/{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}'.format(
    '<string:processor>',
    '<path:imgs>',
    "<int:image_size>",
    "<int:actual_img_width>",
    "<int:surface_x>",
    "<int:surface_z>",
    "<int:has_camera>",
    "<int:cam_h>",
    "<path:fli_file>"
))

if __name__ == "__main__":
    app.run(debug=True)