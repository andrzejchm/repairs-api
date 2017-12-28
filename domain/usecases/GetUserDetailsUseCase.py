from domain.Exceptions import RepairClashException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class GetUserDetailsUseCase(UseCase):
    def __init__(self, users_entity_gateway, username):
        self.users_entity_gateway = users_entity_gateway
        self.username = username

    def execute(self):
        return self.users_entity_gateway.get_user_by_id(self.username)
