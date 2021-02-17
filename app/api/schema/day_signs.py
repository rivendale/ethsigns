"""Module for zodiac schema"""
from app.api import signs_ns
from flask_restplus import fields

day_signs_schema = {
    'id': fields.Integer(description='The Day Sign identifier'),
    'day': fields.String(description='Day Sign Day'),
    'animal': fields.String(description='Day Sign animal')
}

day_signs_schema = signs_ns.model('DaySign', day_signs_schema)
