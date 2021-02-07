from app.api import signs_ns
# from app import api
from flask_restplus.api import Api
from app.api import api_blueprint

authorizations = {'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}
signs_path = "signs/"


api = Api(
    security='Bearer Auth',
    prefix='/api/v1',
    version="1.0",
    doc='/documentation/', authorizations=authorizations)

api.add_namespace(signs_ns, path=signs_path)
# import pdb; pdb.set_trace()