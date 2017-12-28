from domain.Exceptions import RepairClashException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class GetRepairByIdUseCase(UseCase):
    def __init__(self, repairs_entity_gateway, repair_id):
        self.repairs_entity_gateway = repairs_entity_gateway
        self.repair_id = repair_id

    def execute(self):
        return self.repairs_entity_gateway.get_repair_by_id(self.repair_id)
