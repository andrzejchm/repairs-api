from operator import attrgetter

from domain.Exceptions import RepairClashException, RepairNotFoundException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class PostCommentUseCase(UseCase):
    def __init__(self, repairs_entity_gateway, comment):
        self.repairs_entity_gateway = repairs_entity_gateway
        self.comment = comment

    def execute(self):
        return self.repairs_entity_gateway.add_comment(self.comment)
