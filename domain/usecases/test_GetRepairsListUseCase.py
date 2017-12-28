import unittest

from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteRepairEntityGateway import SqliteRepairEntityGateway
from domain.usecases.GetRepairsListUseCase import GetRepairsListUseCase
from config import TEST_DB_URL
from sql_queries import CREATE_REPAIRS_TABLE_QUERY, add_repair_query, COLUMN_START_DATE


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteRepairEntityGateway(self.db)

    def testGetRepairs_startsInWindow(self):
        self.db.execute(add_repair_query(0, 3600, False, False, "andrzejchm"))
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 0, 3000)
        result = useCase.execute()
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].start_date == 0)

    def testGetRepairs_endsInWindow(self):
        self.db.execute(add_repair_query(0, 3600, False, False, "andrzejchm"))
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 4500, 7500)
        result = useCase.execute()
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].start_date == 3600)

    def testGetRepairs_startsAndEndsInWindow(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 0, 10000)
        result = useCase.execute()
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].start_date == 3600)

    def testGetRepairs_repairContainsWindow(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 4000, 7000)
        result = useCase.execute()
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].start_date == 3600)

    def testGetRepairs_repairOutsideWIndow(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 0, 3000)
        result = useCase.execute()
        self.assertTrue(len(result) == 0)

    def testGetRepairs_repairStartMatchStartWindow(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 3600, 7000)
        result = useCase.execute()
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].start_date == 3600)

    def testGetRepairs_repairStartMatchEndWindow(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 0, 3600)
        result = useCase.execute()
        self.assertTrue(len(result) == 0)

    def testGetRepairs_repairEndMatchStartWindow(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 7200, 10800)
        result = useCase.execute()
        self.assertTrue(len(result) == 0)

    def testGetRepairs_showsMultipleMatchingWindow(self):
        self.db.execute(add_repair_query(0, 3600, False, False, "andrzejchm"))
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 0, 7500)
        result = useCase.execute()
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[0].start_date == 0)
        self.assertTrue(result[1].start_date == 3600)

    def testGetRepairs_windowEndTouchesRepairStart(self):
        self.db.execute(add_repair_query(3600, 7200, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 0, 3600)
        result = useCase.execute()
        self.assertTrue(len(result) == 0)

    def testGetRepairs_windowStartTouchesRepaiEnd(self):
        self.db.execute(add_repair_query(0, 3600, False, False, "andrzejchm"))
        useCase = GetRepairsListUseCase(self.entity_gateway, 3600, 7200)
        result = useCase.execute()
        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
