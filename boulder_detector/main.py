from flask import Flask, request
from flask_restful import Api, Resource
import predict
import requests

app = Flask(__name__)
api = Api(app)

class BoulderDetector(Resource):
    def get(self):
        # need to import predict.py
        # call method to predict a single image
        # return json of predicted bounding boxes
        out_img, boulder_list = predict.run(
            processor=request.args.get('processor'),
            imgs=request.args.get('imgs').replace('%2f', '\\'),
            image_size=request.args.get('image_size', type=int),
            #actual_img_width=request.args.get('actual_img_width', type=int),
            surface_x=request.args.get('surface_x', type=int),
            surface_z=request.args.get('surface_z', type=int),
            bl_out_file=request.args.get('bl_out_file').replace('%2f', '\\')
            #has_camera=request.args.get('has_camera', type=int),
            #cam_h=request.args.get('cam_h', type=int),
            #fli_file=request.args.get('fli_file'),
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
        
        return {
            "data": {
                "out_img": out_img,
                "boulder_list": boulder_list
            }
        }

# api endpoint for getting the predicted bounding boxes
api.add_resource(BoulderDetector, '/predict/')

if __name__ == "__main__":
    app.run(debug=True)