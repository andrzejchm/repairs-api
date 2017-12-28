import unittest

import os

from app.App import App
from app.restful.Resources import ResponseSchema
from data.sqlite.RepairsDatabase import RepairsDatabase
from domain.JwtUtils import create_jwt_token
from domain.entities.Comment import CommentSchema, Comment
from domain.entities.Repair import RepairSchema, Repair
from domain.entities.User import User, RegisterUserSchema, RegisterUser, LogInUser, LogInUserSchema, ADMIN_USER_ROLE, \
    DEFAULT_USER_ROLE, MANAGER_USER_ROLE, GetUserSchema
from sql_queries import get_user_by_id_query, COLUMN_USERNAME, COLUMN_PASSWORD_HASH, add_user_query, \
    add_repair_query, get_repair_by_id_query, COLUMN_ID, COLUMN_START_DATE, COLUMN_END_DATE, COLUMN_IS_COMPLETED, \
    COLUMN_PROPOSE_COMPLETE, COLUMN_ASSIGNED_USER, COLUMN_ROLE, add_comment_query, get_repair_comments_query

DB_FILE_NAME = "integration_test_db.db"
INTEGRATION_TEST_DB_URL = f"sqlite:///{DB_FILE_NAME}"

TEST_USERNAME = 'andrzejchm'
TEST_USERNAME2 = 'andrzejchm2'
TEST_PASSWORD = 'password'
TEST_PASSWORD_HASH = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(DB_FILE_NAME)
        except FileNotFoundError:
            pass
        self.app = App(INTEGRATION_TEST_DB_URL)
        self.flaskApp = self.app.init()
        self.client = self.flaskApp.test_client()
        self.db = RepairsDatabase(INTEGRATION_TEST_DB_URL)
        self.auth_token_user = create_jwt_token(User(TEST_USERNAME, TEST_PASSWORD_HASH, DEFAULT_USER_ROLE))
        self.auth_token_manager = create_jwt_token(User(TEST_USERNAME, TEST_PASSWORD_HASH, MANAGER_USER_ROLE))

        # CREATE TESTING DB
        self.db.execute(add_user_query(TEST_USERNAME, TEST_PASSWORD_HASH, DEFAULT_USER_ROLE))
        self.db.execute(add_repair_query(0, 3600, False, True, TEST_USERNAME))
        self.db.execute(add_repair_query(3600, 7200, True, False, TEST_USERNAME))
        self.db.execute(add_comment_query(Comment(None, 1, "this is comment 1", 100, TEST_USERNAME)))
        self.db.execute(add_comment_query(Comment(None, 1, "this is comment 3", 130, TEST_USERNAME)))
        self.db.execute(add_comment_query(Comment(None, 1, "this is comment 2", 120, TEST_USERNAME)))

    def testRegisterUser_success(self):
        # GIVEN
        user = RegisterUser(TEST_USERNAME2, TEST_PASSWORD)
        register_user_json = RegisterUserSchema().dumps(user).data
        # WHEN
        result = self.client.post('/auth/register',
                                  data=register_user_json)
        # THEN
        self.assertEqual(200, result.status_code)
        row = self.db.execute(get_user_by_id_query(TEST_USERNAME2)).fetchone()
        self.assertEqual(TEST_USERNAME2, row[COLUMN_USERNAME])
        self.assertEqual(TEST_PASSWORD_HASH, row[COLUMN_PASSWORD_HASH])
        self.assertEqual(DEFAULT_USER_ROLE, row[COLUMN_ROLE])

    def testRegisterUser_userExists(self):
        # GIVEN
        user = RegisterUser(TEST_USERNAME, TEST_PASSWORD)
        register_user_json = RegisterUserSchema().dumps(user).data
        # WHEN
        result = self.client.post('/auth/register',
                                  data=register_user_json)
        # THEN
        self.assertEqual(403, result.status_code)
        data = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("'andrzejchm' already exists", data['error'])

    def testLogInUser_success(self):
        # GIVEN
        user_json = LogInUserSchema().dumps(LogInUser(TEST_USERNAME, TEST_PASSWORD_HASH)).data
        # WHEN
        result = self.client.post('/auth/login', data=user_json)
        # THEN
        self.assertEqual(200, result.status_code)

        auth_token_headers = [x for x in result.headers if x[0] == 'auth_token']
        self.assertEqual(1, len(auth_token_headers))
        self.assertIsNotNone(auth_token_headers[0][1])

    def testLogInUser_invalidCredentials(self):
        # GIVEN
        user_json = LogInUserSchema().dumps(LogInUser(TEST_USERNAME, "invalid")).data
        # WHEN
        result = self.client.post('/auth/login', data=user_json)
        # THEN
        self.assertEqual(403, result.status_code)

        auth_token_headers = [x for x in result.headers if x[0] == 'auth_token']
        self.assertEqual(0, len(auth_token_headers))

    def testGetRepairs_success(self):
        # GIVEN
        # WHEN
        result = self.client.get('/repairs?from=0&to=7200', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        repairResponse = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        repairs = RepairSchema(many=True).load(repairResponse['payloadArray'])[0]
        self.assertEqual(1, repairs[0].repair_id)
        self.assertEqual(0, repairs[0].start_date)
        self.assertEqual(3600, repairs[0].end_date)
        self.assertEqual('andrzejchm', repairs[0].assigned_user_id)
        self.assertEqual(False, repairs[0].is_completed)
        self.assertEqual(True, repairs[0].propose_complete)

        self.assertEqual(2, repairs[1].repair_id)
        self.assertEqual(3600, repairs[1].start_date)
        self.assertEqual(7200, repairs[1].end_date)
        self.assertEqual('andrzejchm', repairs[1].assigned_user_id)
        self.assertEqual(True, repairs[1].is_completed)
        self.assertEqual(False, repairs[1].propose_complete)

    def testGetRepairs_empty(self):
        # GIVEN
        # WHEN
        result = self.client.get('/repairs?from=10800&to=17200', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        repairResponse = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        repairs = RepairSchema(many=True).load(repairResponse['payloadArray'])[0]
        self.assertEqual(0, len(repairs))

    def testGetRepairById_success(self):
        # GIVEN
        # WHEN
        result = self.client.get('/repairs/1', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        repairResponse = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        repair = RepairSchema().load(repairResponse['payloadDict'])[0]
        self.assertEqual(1, repair.repair_id)
        self.assertEqual(0, repair.start_date)
        self.assertEqual(3600, repair.end_date)
        self.assertEqual('andrzejchm', repair.assigned_user_id)
        self.assertEqual(False, repair.is_completed)
        self.assertEqual(True, repair.propose_complete)

    def testGetRepairById_notFound(self):
        # GIVEN
        # WHEN
        result = self.client.get('/repairs/4', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("There is no repair with id: 4", response['error'])

    def testCreateRepair_success(self):
        # GIVEN
        repair_json = RepairSchema().dumps(Repair(None, 7200, 10800, False, True, TEST_USERNAME)).data
        # WHEN
        result = self.client.put('/repairs', headers=[("Authorization", self.auth_token_user)], data=repair_json)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual(3, response['payloadDict']['repair_id'])

    def testCreateRepair_overlapsFully(self):
        # GIVEN
        repair_json = RepairSchema().dumps(Repair(None, 0, 3600, False, True, TEST_USERNAME)).data
        # WHEN
        result = self.client.put('/repairs', headers=[("Authorization", self.auth_token_user)], data=repair_json)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual('There can be only on repair on given time: <0, 3600)', response['error'])

    def testCreateRepair_overlapsPartiallyOverTwo(self):
        # GIVEN
        repair_json = RepairSchema().dumps(Repair(None, 2600, 6200, False, True, TEST_USERNAME)).data
        # WHEN
        result = self.client.put('/repairs', headers=[("Authorization", self.auth_token_user)], data=repair_json)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual('There can be only on repair on given time: <2600, 6200)', response['error'])

    def testEditRepair_success(self):
        # GIVEN
        repair_json = RepairSchema().dumps(Repair(1, 7200, 10800, True, False, TEST_USERNAME2)).data
        # WHEN
        result = self.client.post('/repairs/1', headers=[("Authorization", self.auth_token_manager)], data=repair_json)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("OK", response['payload'])
        row = self.db.execute(get_repair_by_id_query(1)).fetchone()
        self.assertEqual(1, row[COLUMN_ID])
        self.assertEqual(7200, row[COLUMN_START_DATE])
        self.assertEqual(10800, row[COLUMN_END_DATE])
        self.assertEqual(True, row[COLUMN_IS_COMPLETED])
        self.assertEqual(False, row[COLUMN_PROPOSE_COMPLETE])
        self.assertEqual(TEST_USERNAME2, row[COLUMN_ASSIGNED_USER])

    def testProposeRepairCompletion_alreadyCompleted(self):
        # GIVEN
        repair_id = 2
        # WHEN
        result = self.client.post(f'/repairs/{repair_id}/proposeComplete',
                                  headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("Given repair is already completed. Repair id: 2", response['error'])
        row = self.db.execute(get_repair_by_id_query(repair_id)).fetchone()
        self.assertEqual(0, row[COLUMN_PROPOSE_COMPLETE])
        self.assertEqual(1, row[COLUMN_IS_COMPLETED])

    def testProposeRepairCompletion_success(self):
        # GIVEN
        repair_id = 3
        self.db.execute(add_repair_query(7200, 10800, False, False, TEST_USERNAME))
        # WHEN
        result = self.client.post(f'/repairs/{repair_id}/proposeComplete',
                                  headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("OK", response['payload'])
        row = self.db.execute(get_repair_by_id_query(repair_id)).fetchone()
        self.assertEqual(1, row[COLUMN_PROPOSE_COMPLETE])
        self.assertEqual(0, row[COLUMN_IS_COMPLETED])

    def testMarkRepairCompleted_alreadyCompleted(self):
        # GIVEN
        repair_id = 2
        # WHEN
        result = self.client.post(f'/repairs/{repair_id}/markCompleted',
                                  headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("Given repair is already completed. Repair id: 2", response['error'])
        row = self.db.execute(get_repair_by_id_query(repair_id)).fetchone()
        self.assertEqual(0, row[COLUMN_PROPOSE_COMPLETE])
        self.assertEqual(1, row[COLUMN_IS_COMPLETED])

    def testMarkRepairCompleted_success(self):
        # GIVEN
        repair_id = 3
        self.db.execute(add_repair_query(7200, 10800, False, False, TEST_USERNAME))
        # WHEN
        result = self.client.post(f'/repairs/{repair_id}/markCompleted',
                                  headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("OK", response['payload'])
        row = self.db.execute(get_repair_by_id_query(repair_id)).fetchone()
        self.assertEqual(0, row[COLUMN_PROPOSE_COMPLETE])
        self.assertEqual(1, row[COLUMN_IS_COMPLETED])

    def testMarkRepairCompleted_forbiddenForNormalUsers(self):
        # GIVEN
        repair_id = 3
        self.db.execute(add_repair_query(7200, 10800, False, False, TEST_USERNAME))
        # WHEN
        result = self.client.post(f'/repairs/{repair_id}/markCompleted',
                                  headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])
        row = self.db.execute(get_repair_by_id_query(repair_id)).fetchone()
        self.assertEqual(0, row[COLUMN_PROPOSE_COMPLETE])
        self.assertEqual(0, row[COLUMN_IS_COMPLETED])

    def testEditRepair_overlaps(self):
        # GIVEN
        repair_json = RepairSchema().dumps(Repair(1, 3600, 7200, True, False, TEST_USERNAME2)).data
        # WHEN
        result = self.client.post('/repairs/1', headers=[("Authorization", self.auth_token_manager)], data=repair_json)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("There can be only on repair on given time: <3600, 7200)", response['error'])

    def testEditRepair_forbiddenForNormalUsers(self):
        # GIVEN
        repair_json = RepairSchema().dumps(Repair(1, 7200, 10800, True, False, TEST_USERNAME2)).data
        # WHEN
        result = self.client.post('/repairs/1', headers=[("Authorization", self.auth_token_user)], data=repair_json)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])

    def testDeleteRepair_success(self):
        # GIVEN
        # WHEN
        result = self.client.delete('/repairs/1', headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("OK", response['payload'])
        self.assertEqual(None, self.db.execute(get_repair_by_id_query(1)).fetchone())

    def testDeleteRepair_forbiddenForNormalUsers(self):
        # GIVEN
        # WHEN
        result = self.client.delete('/repairs/1', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])

    def testGetComments_success(self):
        # GIVEN
        # WHEN
        result = self.client.get('/repairs/1/comments', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8')).data
        comments = CommentSchema(many=True).load(response['payloadArray']).data
        self.assertEqual(3, len(comments))
        self.assertEqual("andrzejchm", comments[0].username)
        self.assertEqual("andrzejchm", comments[1].username)
        self.assertEqual("andrzejchm", comments[2].username)
        self.assertEqual("this is comment 1", comments[0].contents)
        self.assertEqual("this is comment 2", comments[1].contents)
        self.assertEqual("this is comment 3", comments[2].contents)

    def testPostComment_success(self):
        # GIVEN
        contents = "this is added comment"
        repair_id = 1
        date = 200
        comment = CommentSchema().dumps(Comment(None, None, contents, date, TEST_USERNAME)).data
        # WHEN
        result = self.client.put('/repairs/1/comments', headers=[("Authorization", self.auth_token_user)], data=comment)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8')).data
        self.assertEqual("OK", response['payload'])
        result = self.db.execute(get_repair_comments_query(repair_id))
        comments = []
        for row in result:
            comments.append(CommentSchema().load(CommentSchema().dump(row).data).data)
        self.assertEqual(4, len(comments))
        self.assertEqual(date, comments[3].date)
        self.assertEqual(contents, comments[3].contents)
        self.assertEqual(TEST_USERNAME, comments[3].username)

    def testPostComment_repairDoesNotExist(self):
        # GIVEN
        contents = "this is added comment"
        repair_id = 1
        date = 200
        comment = CommentSchema().dumps(Comment(None, None, contents, date, TEST_USERNAME)).data
        # WHEN
        result = self.client.put('/repairs/4/comments', headers=[("Authorization", self.auth_token_user)], data=comment)
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8')).data
        self.assertEqual("There is no repair with id: 4", response['error'])

    def testGetUsers_forbiddenForNormalUsers(self):
        # GIVEN
        # WHEN
        result = self.client.get('/users', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])

    def testGetUsers_success(self):
        # GIVEN
        # WHEN
        result = self.client.get('/users', headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8')).data
        users = GetUserSchema(many=True).load(response['payloadArray']).data
        self.assertEqual(1, len(users))
        self.assertEqual("andrzejchm", users[0].username)
        self.assertIsNone(users[0].password_hash)

    def testGetUserDetails_forbiddenForNormalUsers(self):
        # GIVEN
        # WHEN
        result = self.client.get(f'/users/{TEST_USERNAME}', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])

    def testGetUserDetails_success(self):
        # GIVEN
        # WHEN
        result = self.client.get(f'/users/{TEST_USERNAME}', headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8')).data
        user = GetUserSchema().load(response['payloadDict']).data
        self.assertEqual("andrzejchm", user.username)
        self.assertIsNone(user.password_hash)

    def searchUsers_forbiddenForNormalUsers(self):
        # GIVEN
        # WHEN
        result = self.client.get(f'/users/search?q=rzejc', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])

    def searchUsers_success(self):
        # GIVEN
        self.db.execute(add_user_query(TEST_USERNAME2, TEST_PASSWORD_HASH, DEFAULT_USER_ROLE))
        # WHEN
        result = self.client.get(f'/users/search?q=rzejc', headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8')).data
        users = GetUserSchema(many=True).load(response['payloadArray']).data
        self.assertEqual(2, len(users))
        self.assertEqual("andrzejchm", users[0].username)
        self.assertIsNone(users[0].password_hash)
        self.assertEqual("andrzejchm2", users[1].username)
        self.assertIsNone(users[0].password_hash)

    def testDeleteUser_success(self):
        # GIVEN
        self.db.execute(add_user_query(TEST_USERNAME2, TEST_PASSWORD_HASH, DEFAULT_USER_ROLE))
        # WHEN
        result = self.client.delete(f'/users/{TEST_USERNAME2}', headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("OK", response['payload'])
        self.assertEqual(None, self.db.execute(get_user_by_id_query(TEST_USERNAME2)).fetchone())
        self.assertIsNotNone(self.db.execute(get_user_by_id_query(TEST_USERNAME)).fetchone())

    def testDeleteUser_forbiddenForNormalUsers(self):
        # GIVEN
        # WHEN
        result = self.client.delete(f'/users/{TEST_USERNAME}', headers=[("Authorization", self.auth_token_user)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You must be at least manager to perform this operation", response['error'])

    def testDeleteUser_cantDeleteSelf(self):
        # GIVEN
        # WHEN
        result = self.client.delete(f'/users/{TEST_USERNAME}', headers=[("Authorization", self.auth_token_manager)])
        # THEN
        self.assertEqual(200, result.status_code)
        response = ResponseSchema().loads(result.data.decode('utf-8'))[0]
        self.assertEqual("You cannot delete your own user", response['error'])

    def tearDown(self):
        os.remove(DB_FILE_NAME)


if __name__ == '__main__':
    unittest.main()
