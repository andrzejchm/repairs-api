from domain.Exceptions import RepairClashException
from domain.usecases.UseCase import UseCase


class CreateRepairUseCase(UseCase):
    def __init__(self, repairs_entity_gateway, repair):
        self.repairs_entity_gateway = repairs_entity_gateway
        self.repair = repair

    def execute(self):
        self.repair.validate()
        repairs = self.repairs_entity_gateway.get_repairs_in_date_range(self.repair.start_date, self.repair.end_date)
        if len(repairs) > 0:
            raise RepairClashException(self.repair.start_date, self.repair.end_date)
        return self.repairs_entity_gateway.create_repair(self.repair)
