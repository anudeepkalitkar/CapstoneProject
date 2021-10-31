import pandas as pd
import numpy as np
from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from apispec import APISpec
from flask_cors import CORS, cross_origin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from Model.Model import trainModel, predictTopic
global LRModel
global pipelineFit
global mappedLabels
app = Flask(__name__)  
CORS(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Capstone RestAPIs',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/documentationJson',
    'APISPEC_SWAGGER_UI_URL': '/'
})
api = Api(app)

class pingResParams(Schema):
    ping = fields.String(required=True, description="Project pinged")
class ping(MethodResource, Resource):
    @doc(description='ping', tags=['ping'])
    @cross_origin()
    @marshal_with(pingResParams)
    def get(self):
        return {'ping':'pong'}


class train(MethodResource, Resource):
    @doc(description='train', tags=['train'])
    @cross_origin()
    def get(self):
        global LRModel
        global pipelineFit
        global mappedLabels
        try:
            LRModel, pipelineFit, mappedLabels = trainModel()
            return {'Success':'True'}
        except: 
            return {'Success':'False'}


class predictReqParams(Schema):
    searchText = fields.String(required=True, description="search Text")
class predict(MethodResource, Resource):
    @doc(description='predict', tags=['predict'])
    @cross_origin()
    @use_kwargs(predictReqParams, location=('json'))
    def post(self,**args):
        params = [["","","","",args['searchText'],"","news"]]
        DataFields=["title","published_date","link","clean_url","summary","media","topic"]
        data = np.array(params)
        data = pd.DataFrame(data = data,columns=DataFields)
        prediction = predictTopic(LRModel,pipelineFit,data)
        result = mappedLabels[int(prediction)]
        return {'category': result}

api.add_resource(ping, '/ping')
api.add_resource(train, '/train')
api.add_resource(predict, '/predict')
docs = FlaskApiSpec(app)
docs.register(ping)
docs.register(train)
docs.register(predict)
# app.get('/train')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=1234)



# "Elon Musk, the billionaire CEO of electric car manufacturers Tesla, has caused ripples through the cryptocurrency market again. On Monday, he posted a picture of his new Shiba Inu puppy, Floki Funkpuppy, boosting the token of the same name and inspiring a new addition that has already started flying. His inspiration has helped many novice investors try their hand at cryptocurrencies, but also led experts to ask questions.Mr Musk's ongoing influence underlines the inherent volatility behind altco",
