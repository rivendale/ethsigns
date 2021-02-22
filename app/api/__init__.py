from flask import Blueprint
from flask_restplus import Namespace

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api/v1')

signs_ns = Namespace("signs", description="signs operations")
