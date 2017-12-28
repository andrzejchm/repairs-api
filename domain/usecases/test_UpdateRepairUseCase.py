import unittest

from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteRepairEntityGateway import SqliteRepairEntityGateway
from domain.Exceptions import RepairNotFoundException
from domain.entities.Repair import Repair
from domain.usecases.GetRepairByIdUseCase import GetRepairByIdUseCase
from domain.usecases.UpdateRepairUseCase import UpdateRepairUseCase
from config import TEST_DB_URL
from sql_queries import CREATE_REPAIRS_TABLE_QUERY, add_repair_query, get_repair_by_id_query, COLUMN_ASSIGNED_USER, \
    COLUMN_ID, COLUMN_START_DATE, COLUMN_END_DATE, COLUMN_IS_COMPLETED, COLUMN_PROPOSE_COMPLETE


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteRepairEntityGateway(self.db)

    def testUpdateRepair_updatesAllFields(self):
        self.db.execute(add_repair_query(0, 3600, False, True, "andrzejchm"))
        useCase = UpdateRepairUseCase(self.entity_gateway, Repair(1,1,3601,True,False,"changed"))
        useCase.execute()
        row = self.db.execute(get_repair_by_id_query(1)).fetchone()
        self.assertEqual("changed", row[COLUMN_ASSIGNED_USER])
        self.assertEqual(1, row[COLUMN_ID])
        self.assertEqual(1, row[COLUMN_START_DATE])
        self.assertEqual(3601, row[COLUMN_END_DATE])
        self.assertTrue(row[COLUMN_IS_COMPLETED])
        self.assertFalse(row[COLUMN_PROPOSE_COMPLETE])

    def testUpdateRepair_raisesWhenNoRepair(self):
        useCase = UpdateRepairUseCase(self.entity_gateway, Repair(1,1,3601,True,False,"changed"))
        with self.assertRaises(RepairNotFoundException):
            useCase.execute()

if __name__ == '__main__':
    unittest.main()
