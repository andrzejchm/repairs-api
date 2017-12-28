from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteRepairEntityGateway import SqliteRepairEntityGateway
from data.sqlite.gateways.SqliteUserEntityGateway import SqliteUserEntityGateway
from domain.usecases.UseCaseFactory import UseCaseFactory


class DependencyInjector:
    def __init__(self, db_url):
        self.db_url = db_url

    def provide_repairs_db(self):
        return RepairsDatabase(self.db_url)

    def provide_users_entity_gateway(self):
        return SqliteUserEntityGateway(self.provide_repairs_db())

    def provide_repairs_entity_gateway(self):
        return SqliteRepairEntityGateway(self.provide_repairs_db())

    def provide_use_case_factory(self):
        return UseCaseFactory(self.provide_users_entity_gateway(),
                              self.provide_repairs_entity_gateway())
