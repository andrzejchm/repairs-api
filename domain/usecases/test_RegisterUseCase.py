import unittest

from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteUserEntityGateway import SqliteUserEntityGateway
from domain.entities.User import DEFAULT_USER_ROLE
from domain.Exceptions import UserAlreadyExistsException
from domain.usecases.RegisterUserUseCase import hashPassword, RegisterUserUseCase
from config import TEST_DB_URL
from sql_queries import get_user_by_id_query, COLUMN_ROLE


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteUserEntityGateway(self.db)

    def testGivenUserCanBeRegisteredOnlyOnce(self):
        useCase = RegisterUserUseCase(self.entity_gateway, "andrzejchm", "password")
        useCase.execute()
        with self.assertRaises(UserAlreadyExistsException):
            useCase.execute()

    def testHashPasswordUsesSHA1(self):
        self.assertEqual(hashPassword('password'), "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8")

    def testCreatesUserWithDefaultRole(self):
        useCase = RegisterUserUseCase(self.entity_gateway, "andrzejchm", "password")
        useCase.execute()
        row = self.db.execute(get_user_by_id_query("andrzejchm")).fetchone()
        self.assertEqual(DEFAULT_USER_ROLE, row[COLUMN_ROLE])


if __name__ == '__main__':
    unittest.main()
