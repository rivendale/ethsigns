"""Module for zodiac schema"""
import calendar

from app.api import signs_ns
from flask_restplus import fields

month_signs_schema = {
    'id': fields.Integer(description='The Month Sign identifier'),
    'month': fields.String(description='Month Sign month',
                           attribute=lambda x: calendar.month_name[x.month]),
    'animal': fields.String(description='Month Sign animal')
}

month_signs_schema = signs_ns.model('MonthSign', month_signs_schema)
