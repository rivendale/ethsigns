from flask_restplus import fields
from app.api import signs_ns


admin_schema = {
    'wallet_balance': fields.Float(description='Wallet balance'),
}
admin_schema = signs_ns.model('Admin', admin_schema)
