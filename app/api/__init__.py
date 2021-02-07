from flask_restplus import Namespace
from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api/v1')

signs_ns = Namespace("signs", description="signs operations")
