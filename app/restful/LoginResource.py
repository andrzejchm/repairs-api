from flask_restful import abort
from flask import request

from app.restful.Resources import ApiAnonymousResource, errorResponseString
from domain.entities.User import UserSchema, LogInUserSchema


class LoginResource(ApiAnonymousResource):
    def post(self, **kwargs):
        user = LogInUserSchema().load(request.get_json(force=True)).data
        jwt_token = self.use_case_factory.log_in_use_case(user.username, user.password_hash).execute()
        if jwt_token:
            return "OK", 200, { 'auth_token': jwt_token}
        else:
            abort(403, **errorResponseString("Invalid credentials", 403))
