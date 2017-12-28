from domain.Exceptions import RepairClashException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class SearchUsersUseCase(UseCase):
    def __init__(self, users_entity_gateway, query):
        self.users_entity_gateway = users_entity_gateway
        self.query = query

    def execute(self):
        return self.users_entity_gateway.search_users(self.query)
