from domain.Exceptions import UserAlreadyExistsException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


def hashPassword(password):
    import hashlib
    sha = hashlib.sha1()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()


class RegisterUserUseCase(UseCase):
    def __init__(self, users_entity_gateway, username, password):
        self.users_entity_gateway = users_entity_gateway
        self.username = username
        self.password = password

    def execute(self):
        user = self.users_entity_gateway.get_user_by_id(self.username)
        if user:
            raise UserAlreadyExistsException(self.username)
        else:
            return self.users_entity_gateway.create_user(self.username, hashPassword(self.password))
