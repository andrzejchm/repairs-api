import datetime
from functools import wraps
from flask import request
from flask_restful import abort

from domain.JwtUtils import parse_jwt_token
from domain.entities.User import User


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        authToken = request.headers['Authorization']
        try:
            username, timestamp, role = parse_jwt_token(authToken)
        except:
            abort(401)
            return
        if timestamp > datetime.datetime.now().timestamp():
            return func(user=User(username, None, role), *args, **kwargs)
        else:
            abort(401)

    return wrapper
