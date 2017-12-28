from domain.Exceptions import UserAlreadyExistsException, UserNotFoundException
from domain.entities.User import User, DEFAULT_USER_ROLE, UserSchema, GetUserSchema
from domain.gateways.UserEntityGateway import UserEntityGateway
from sql_queries import COLUMN_USERNAME, COLUMN_PASSWORD_HASH, get_user_by_id_query, add_user_query, COLUMN_ROLE, \
    get_users_query, seach_users_query, delete_user_query


class SqliteUserEntityGateway(UserEntityGateway):
    def __init__(self, repairs_db):
        self.repairs_db = repairs_db

    def get_user_by_id(self, user_id):
        result = self.repairs_db.execute(get_user_by_id_query(user_id))
        for row in result:
            if row[COLUMN_USERNAME] == user_id:
                return User(row[COLUMN_USERNAME], row[COLUMN_PASSWORD_HASH], row[COLUMN_ROLE])
        return None

    def create_user(self, user_id, passwordHash):
        user = self.get_user_by_id(user_id)
        if user:
            raise UserAlreadyExistsException(user_id)
        else:
            self.repairs_db.execute(add_user_query(user_id, passwordHash, DEFAULT_USER_ROLE))

    def get_users(self):
        result = self.repairs_db.execute(get_users_query())
        users = []
        for row in result:
            user = User(row[COLUMN_USERNAME], row[COLUMN_PASSWORD_HASH], row[COLUMN_ROLE])
            users.append(user)
        return users

    def search_users(self, query):
        result = self.repairs_db.execute(seach_users_query(query))
        users = []
        for row in result:
            user = User(row[COLUMN_USERNAME], row[COLUMN_PASSWORD_HASH], row[COLUMN_ROLE])
            users.append(user)
        return users

    def delete_user(self, username):
        result = self.repairs_db.execute(delete_user_query(username))
        if result.rowcount != 1:
            raise UserNotFoundException(username)



