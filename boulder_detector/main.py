from flask import Flask
from flask_restful import Api, Resource
import predict
import requests

app = Flask(__name__)
api = Api(app)

class BoulderDetector(Resource):
    def get(self, image, processor):
        # need to import predict.py
        # call method to predict a single image
        # return json of predicted bounding boxes
        result = predict.run(
            imgs=image,
            processor=processor
        )
        
        return result

class MakeBoulderList(Resource):
    def get(self):
        pass

# api endpoint for getting the predicted bounding boxes
api.add_resource(BoulderDetector, '/predict/{0}/{1}'.format(
    '<path:image>',
    '<string:processor>'
))

if __name__ == "__main__":
    app.run(debug=True)