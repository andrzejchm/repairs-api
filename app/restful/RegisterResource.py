from flask_restful import abort
from flask import request

from app.restful.Resources import errorResponse, successResponse, ApiAnonymousResource, errorResponseString
from domain.Exceptions import ApiException


class RegisterResource(ApiAnonymousResource):
    def post(self, **kwargs):
        data = request.get_json(force=True)
        try:
            self.use_case_factory.register_user_use_case(data['username'], data['password']).execute()
            return successResponse("OK")
        except ApiException as error:
            abort(403, **errorResponse(error))
