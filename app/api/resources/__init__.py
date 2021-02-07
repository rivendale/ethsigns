# from app.api import signs_ns
from flask_restplus.api import Api

authorizations = {'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}
# signs_path = "signs/"


api = Api(
    security='Bearer Auth',
    prefix='/api/v1',
    version="1.0",
    doc=False, authorizations=authorizations)

# api.add_namespace(signs_ns, path=signs_path)
