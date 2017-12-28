from domain.usecases.UseCase import UseCase


class GetRepairsListUseCase(UseCase):
    def __init__(self, repairs_entity_gateway, from_timestamp_inclusive, to_timestamp_exclusive):
        self.repairs_entity_gateway = repairs_entity_gateway
        self.from_timestamp_inclusive = from_timestamp_inclusive
        self.to_timestamp_exclusive = to_timestamp_exclusive

    def execute(self):
        return self.repairs_entity_gateway.get_repairs_in_date_range(self.from_timestamp_inclusive,
                                                                     self.to_timestamp_exclusive)


