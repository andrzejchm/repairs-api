from flask_restful import Resource
from marshmallow import fields, Schema

from app.restful.ApiMethodWrappers import authenticated

USE_CASE_FACTORY = 'use_case_factory'


def get_user(**kwargs):
    return kwargs['user']


class ApiAuthenticatedResource(Resource):
    method_decorators = [authenticated]

    def __init__(self, **kwargs):
        self.use_case_factory = kwargs[USE_CASE_FACTORY]


class ApiAnonymousResource(Resource):
    def __init__(self, **kwargs):
        self.use_case_factory = kwargs[USE_CASE_FACTORY]


def errorResponseString(errorMessage, code):
    return {'error': errorMessage, 'code': code}


def errorResponse(error):
    return {'error': error.message, 'code': error.error_code}


def successResponse(payload):
    return {'payload': payload}


class ResponseSchema(Schema):
    error = fields.Str(required=False)
    code = fields.Int(required=True)
    payload = fields.Str(required=False)
    payloadArray = fields.List(fields.Dict(), load_from='payload')
    payloadDict = fields.Dict(load_from='payload')
