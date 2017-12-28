import unittest

from config import TEST_DB_URL
from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteRepairEntityGateway import SqliteRepairEntityGateway
from domain.Exceptions import RepairClashException
from domain.entities.Repair import Repair
from domain.usecases.CreateRepairUseCase import CreateRepairUseCase


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteRepairEntityGateway(self.db)

    def test_createRepairReturnsId(self):
        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 0, 3600, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(1, result)

        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 3600, 7200, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(2, result)

    def test_cantCreateRepairThatClashesWithOther(self):
        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 0, 3600, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(1, result)

        with self.assertRaises(RepairClashException):
            useCase.execute()

    def test_createRepairJustAfterPrevious(self):
        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 0, 3600, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(1, result)
        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 3600, 7200, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(2, result)

    def test_createRepairJustBeforeNext(self):
        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 3600, 7200, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(1, result)
        useCase = CreateRepairUseCase(self.entity_gateway, Repair(None, 0, 3600, False, False, "andrzejchm"))
        result = useCase.execute()
        self.assertEqual(2, result)


if __name__ == '__main__':
    unittest.main()
