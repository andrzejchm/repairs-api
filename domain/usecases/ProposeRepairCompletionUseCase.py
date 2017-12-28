from domain.Exceptions import RepairClashException, RepairAlreadyCompletedException
from domain.usecases.UseCase import UseCase
import jwt
import datetime


class ProposeRepairCompletionUseCase(UseCase):
    def __init__(self, repairs_entity_gateway, repair_id):
        self.repairs_entity_gateway = repairs_entity_gateway
        self.repair_id = repair_id

    def execute(self):
        repair = self.repairs_entity_gateway.get_repair_by_id(self.repair_id)
        if repair.is_completed:
            raise RepairAlreadyCompletedException(self.repair_id)
        return self.repairs_entity_gateway.propose_repair_completion(self.repair_id)
