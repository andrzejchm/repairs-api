import unittest

from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteRepairEntityGateway import SqliteRepairEntityGateway
from domain.Exceptions import RepairNotFoundException
from domain.usecases.GetRepairByIdUseCase import GetRepairByIdUseCase
from config import TEST_DB_URL
from sql_queries import CREATE_REPAIRS_TABLE_QUERY, add_repair_query


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteRepairEntityGateway(self.db)

    def testGetRepair_returnsFoundRepair(self):
        self.db.execute(add_repair_query(0, 3600, False, True, "andrzejchm"))
        useCase = GetRepairByIdUseCase(self.entity_gateway, 1)
        result = useCase.execute()
        self.assertEqual("andrzejchm", result.assigned_user_id)
        self.assertEqual(1, result.repair_id)
        self.assertEqual(0, result.start_date)
        self.assertEqual(3600, result.end_date)
        self.assertFalse(result.is_completed)
        self.assertTrue(result.propose_complete)

    def testGetRepair_throwsWhenNoRepair(self):
        useCase = GetRepairByIdUseCase(self.entity_gateway, 1)
        with self.assertRaises(RepairNotFoundException):
            useCase.execute()


if __name__ == '__main__':
    unittest.main()
