# TABLES
TABLE_USERS = 'Users'
TABLE_REPAIRS = 'Repairs'
TABLE_COMMENTS = 'Comments'

# COLUMNS
COLUMN_USERNAME = 'username'
COLUMN_PASSWORD_HASH = 'passwordHash'
COLUMN_ROLE = 'role'
COLUMN_ID = "id"
COLUMN_REPAIR_ID = "repair_id"
COLUMN_START_DATE = "startDate"
COLUMN_END_DATE = "endDate"
COLUMN_IS_COMPLETED = "isCompleted"
COLUMN_PROPOSE_COMPLETE = "proposeComplete"
COLUMN_ASSIGNED_USER = "assignedUser"
COLUMN_CONTENTS = "contents"
COLUMN_DATE = "date"

CREATE_USERS_TABLE_QUERY = f"CREATE TABLE `{TABLE_USERS}` ( " \
                           f"`{COLUMN_USERNAME}` TEXT NOT NULL UNIQUE," \
                           f"`{COLUMN_PASSWORD_HASH}` TEXT NOT NULL," \
                           f"`{COLUMN_ROLE}` TEXT NOT NULL," \
                           f" PRIMARY KEY(`{COLUMN_USERNAME}`) )"

CREATE_REPAIRS_TABLE_QUERY = f"CREATE TABLE `{TABLE_REPAIRS}` (" \
                             f"`{COLUMN_ID}`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE," \
                             f"`{COLUMN_START_DATE}`	INTEGER NOT NULL," \
                             f"`{COLUMN_END_DATE}`	INTEGER NOT NULL," \
                             f"`{COLUMN_IS_COMPLETED}`	INTEGER NOT NULL," \
                             f"`{COLUMN_PROPOSE_COMPLETE}`	INTEGER NOT NULL," \
                             f"`{COLUMN_ASSIGNED_USER}`	TEXT," \
                             f"FOREIGN KEY(`{COLUMN_ASSIGNED_USER}`) REFERENCES `{TABLE_USERS}`(`{COLUMN_USERNAME}`) " \
                             f"ON DELETE SET NULL ON UPDATE CASCADE)"

CREATE_COMMENTS_TABLE_QUERY = f"CREATE TABLE `{TABLE_COMMENTS}` ( " \
                              f"`{COLUMN_ID}` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE," \
                              f"`{COLUMN_REPAIR_ID}` INTEGER NOT NULL," \
                              f"`{COLUMN_CONTENTS}` TEXT NOT NULL," \
                              f"`{COLUMN_DATE}` INTEGER NOT NULL," \
                              f"`{COLUMN_USERNAME}` INTEGER NOT NULL," \
                              f" FOREIGN KEY(`{COLUMN_USERNAME}`) REFERENCES `{TABLE_USERS}`(`{COLUMN_USERNAME}`)" \
                              f" ON DELETE SET NULL ON UPDATE CASCADE, " \
                              f" FOREIGN KEY(`{COLUMN_REPAIR_ID}`) REFERENCES `{TABLE_REPAIRS}`(`{COLUMN_ID}`)" \
                              f" ON DELETE SET NULL ON UPDATE CASCADE) "


def bool_to_int(boolean):
    return 1 if boolean else 0


def get_users_query():
    return f"SELECT * FROM `{TABLE_USERS}`"


def seach_users_query(query):
    return f"SELECT * FROM `{TABLE_USERS}` WHERE `{COLUMN_USERNAME} LIKE '%{query}%'"


def delete_user_query(username):
    return f"DELETE FROM `{TABLE_USERS}` WHERE `{COLUMN_USERNAME}` = '{username}'"


def add_user_query(username, passwordHash, role):
    return f"INSERT INTO `{TABLE_USERS}`(`{COLUMN_USERNAME}`,`{COLUMN_PASSWORD_HASH}`,`{COLUMN_ROLE}`) " \
           f"VALUES (\"{username.strip()}\", \"{passwordHash.strip()}\", \"{role.strip()}\");"


def get_user_by_id_query(user_id):
    return f"SELECT * FROM `{TABLE_USERS}` WHERE {COLUMN_USERNAME} = \"{user_id.strip()}\""


def get_repairs_in_date_range_query(from_inclusive, to_exclusive):
    return f"SELECT * FROM `{TABLE_REPAIRS}`" \
           f" WHERE (`{COLUMN_START_DATE}` >= {from_inclusive}  AND `{COLUMN_START_DATE}` < {to_exclusive}) " \
           f"OR  (`{COLUMN_END_DATE}` > {from_inclusive}  AND `{COLUMN_END_DATE}` < {to_exclusive})" \
           f"OR  (`{COLUMN_START_DATE}` < {from_inclusive}  AND `{COLUMN_END_DATE}` >= {to_exclusive})"


def add_repair_query(start_date, end_date, is_completed, propose_complete, assigned_user_id):
    return f"INSERT INTO `{TABLE_REPAIRS}`" \
           f"(`{COLUMN_START_DATE}`," \
           f"`{COLUMN_END_DATE}`," \
           f"`{COLUMN_IS_COMPLETED}`," \
           f"`{COLUMN_PROPOSE_COMPLETE}`," \
           f"`{COLUMN_ASSIGNED_USER}`) " \
           f"VALUES" \
           f" ({start_date}," \
           f"{end_date}," \
           f"{bool_to_int(is_completed)}," \
           f"{bool_to_int(propose_complete)}," \
           f"\"{assigned_user_id}\");"


def get_repair_by_id_query(repair_id):
    return f"SELECT * FROM `{TABLE_REPAIRS}` WHERE `{COLUMN_ID}` = {repair_id}"


def delete_repair_by_id_query(repair_id):
    return f"DELETE FROM `{TABLE_REPAIRS}` WHERE `{COLUMN_ID}` = {repair_id}"


def update_repair_by_id_query(repair):
    return f"UPDATE `{TABLE_REPAIRS}` SET " \
           f"`{COLUMN_END_DATE}` = {repair.end_date}, " \
           f"`{COLUMN_START_DATE}` = {repair.start_date}, " \
           f"`{COLUMN_IS_COMPLETED}` = {bool_to_int(repair.is_completed)}, " \
           f"`{COLUMN_PROPOSE_COMPLETE}` = {bool_to_int(repair.propose_complete)}, " \
           f"`{COLUMN_ASSIGNED_USER}` = '{repair.assigned_user_id}' " \
           f"WHERE `{COLUMN_ID}` = {repair.repair_id};"


def propose_repair_completion_query(repair_id):
    return f"UPDATE `{TABLE_REPAIRS}` SET " \
           f"`{COLUMN_PROPOSE_COMPLETE}` = {bool_to_int(True)} " \
           f"WHERE `{COLUMN_ID}` = {repair_id};"


def mark_repair_completed_query(repair_id):
    return f"UPDATE `{TABLE_REPAIRS}` SET " \
           f"`{COLUMN_IS_COMPLETED}` = {bool_to_int(True)}, " \
           f"`{COLUMN_PROPOSE_COMPLETE}` = {bool_to_int(False)} " \
           f"WHERE `{COLUMN_ID}` = {repair_id};"


def get_repair_comments_query(repair_id):
    return f"SELECT * FROM `{TABLE_COMMENTS}` WHERE `{COLUMN_REPAIR_ID}` = {repair_id}"


def add_comment_query(comment):
    return f"INSERT INTO `{TABLE_COMMENTS}`" \
           f"(`{COLUMN_REPAIR_ID}`," \
           f"`{COLUMN_CONTENTS}`," \
           f"`{COLUMN_DATE}`," \
           f"`{COLUMN_USERNAME}`) " \
           f"VALUES" \
           f" ({comment.repair_id}," \
           f"\"{comment.contents}\"," \
           f"{comment.date}," \
           f"\"{comment.username}\")"
