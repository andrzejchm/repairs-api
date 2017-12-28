from domain.JwtUtils import create_jwt_token
from domain.usecases.UseCase import UseCase


class LogInUseCase(UseCase):
    def __init__(self, users_entity_gateway, username, password_hash):
        self.users_entity_gateway = users_entity_gateway
        self.username = username
        self.password_hash = password_hash

    def execute(self):
        user = self.users_entity_gateway.get_user_by_id(self.username)
        if user and user.password_hash == self.password_hash:
            return create_jwt_token(user)
        else:
            return None
