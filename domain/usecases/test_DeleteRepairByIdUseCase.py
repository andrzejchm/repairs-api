import unittest

from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteRepairEntityGateway import SqliteRepairEntityGateway
from domain.Exceptions import RepairNotFoundException
from domain.usecases.DeleteRepairByIdUseCase import DeleteRepairByIdUseCase
from config import TEST_DB_URL
from sql_queries import CREATE_REPAIRS_TABLE_QUERY, add_repair_query, COLUMN_START_DATE, get_repair_by_id_query


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteRepairEntityGateway(self.db)

    def testDeleteRepair_deletesSuccessfuly(self):
        self.db.execute(add_repair_query(0, 3600, False, True, "andrzejchm"))
        self.assertIsNotNone(self.db.execute(get_repair_by_id_query(1)).fetchone())
        useCase = DeleteRepairByIdUseCase(self.entity_gateway,1)
        useCase.execute()
        self.assertIsNone(self.db.execute(get_repair_by_id_query(1)).fetchone())

    def testDeleteRepair_throwsWhenNoRepair(self):
        useCase = DeleteRepairByIdUseCase(self.entity_gateway,1)
        with self.assertRaises(RepairNotFoundException):
            useCase.execute()

if __name__ == '__main__':
    unittest.main()
