from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from sql_queries import CREATE_USERS_TABLE_QUERY, CREATE_REPAIRS_TABLE_QUERY, CREATE_COMMENTS_TABLE_QUERY


class RepairsDatabase:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        try:
            self.engine.execute(CREATE_USERS_TABLE_QUERY)
        except OperationalError as ex:
            pass
        try:
            self.engine.execute(CREATE_REPAIRS_TABLE_QUERY)
        except OperationalError as ex:
            pass
        try:
            self.engine.execute(CREATE_COMMENTS_TABLE_QUERY)
        except OperationalError as ex:
            pass

    def execute(self, query):
        connection = self.engine.connect()
        result = self.engine.execute(query)
        connection.close()
        return result