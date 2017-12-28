from operator import attrgetter

from domain.Exceptions import RepairClashException, RepairNotFoundException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class GetRepairCommentsUseCase(UseCase):
    def __init__(self, repairs_entity_gateway, repair_id):
        self.repairs_entity_gateway = repairs_entity_gateway
        self.repair_id = repair_id

    def execute(self):
        comments = self.repairs_entity_gateway.get_repair_comments(self.repair_id)
        comments.sort(key=attrgetter('date'))
        return comments
