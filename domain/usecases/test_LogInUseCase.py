import unittest

from config import TEST_DB_URL
from domain.entities.User import DEFAULT_USER_ROLE
from sql_queries import CREATE_USERS_TABLE_QUERY, add_user_query
from data.sqlite.RepairsDatabase import RepairsDatabase
from data.sqlite.gateways.SqliteUserEntityGateway import SqliteUserEntityGateway
from domain.usecases.LogInUseCase import LogInUseCase


class TestsWithDb(unittest.TestCase):
    def setUp(self):
        self.db = RepairsDatabase(TEST_DB_URL)
        self.entity_gateway = SqliteUserEntityGateway(self.db)

    def testUserNotFoundReturnsNone(self):
        useCase = LogInUseCase(self.entity_gateway, "andrzejchm", "hash1")
        self.assertIsNone(useCase.execute())

    def testInvalidPasswordReturnsNone(self):
        username = 'user1'
        self.db.execute(add_user_query(username, "passwordHash", DEFAULT_USER_ROLE))
        useCase = LogInUseCase(self.entity_gateway, username, "invalidHash")
        self.assertIsNone(useCase.execute())

    def testValidCredentialsReturnJWTToken(self):
        username = 'user1'
        password_hash = 'hash'
        role = 'user'
        self.db.execute(add_user_query(username, password_hash, role))
        use_case = LogInUseCase(self.entity_gateway, username, password_hash)
        token = use_case.execute()
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)


if __name__ == '__main__':
    unittest.main()
