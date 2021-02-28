from flask_restplus import Namespace, fields

class IADto:
    api = Namespace('ia', description='ia related operations')
    model = api.model('ia', {
        'CourtAbreviation': fields.String(required=True, description='court abreviation'),
        'Year': fields.String(required=True, description='matter year'),
        'Class': fields.String(required=True, description='matter class'),
        'CourtEntry': fields.String(description='court entry'),
        'CourtDecisor': fields.String(description='court decisor'),
        'CourtSession': fields.String(description='court session'),
    })