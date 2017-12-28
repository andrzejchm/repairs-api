from domain.Exceptions import RepairClashException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class GetUsersUseCase(UseCase):
    def __init__(self, users_entity_gateway):
        self.users_entity_gateway = users_entity_gateway

    def execute(self):
        users = self.users_entity_gateway.get_users()
        for user in users:
            user.password_hash = None
        return users
