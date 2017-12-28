from domain.Exceptions import InvalidDateRangeException, RepairNotFoundException, CommentPostFailedException
from domain.entities.Comment import CommentSchema
from domain.entities.Repair import Repair
from domain.gateways.RepairEntityGateway import RepairEntityGateway
from sql_queries import get_repairs_in_date_range_query, COLUMN_ID, COLUMN_START_DATE, COLUMN_END_DATE, \
    COLUMN_IS_COMPLETED, COLUMN_PROPOSE_COMPLETE, COLUMN_ASSIGNED_USER, add_repair_query, get_repair_by_id_query, \
    delete_repair_by_id_query, update_repair_by_id_query, propose_repair_completion_query, mark_repair_completed_query, \
    get_repair_comments_query, add_comment_query


def repair_from_row(row):
    return Repair(
        row[COLUMN_ID],
        row[COLUMN_START_DATE],
        row[COLUMN_END_DATE],
        True if row[COLUMN_IS_COMPLETED] else False,
        True if row[COLUMN_PROPOSE_COMPLETE] else False,
        row[COLUMN_ASSIGNED_USER],
    )


class SqliteRepairEntityGateway(RepairEntityGateway):
    def __init__(self, repairs_db):
        self.repairs_db = repairs_db

    def get_repairs_in_date_range(self, from_timestamp_inclusive, to_timestamp_exclusive):
        if to_timestamp_exclusive <= from_timestamp_inclusive:
            raise InvalidDateRangeException(from_timestamp_inclusive, to_timestamp_exclusive)
        query = get_repairs_in_date_range_query(from_timestamp_inclusive, to_timestamp_exclusive)
        result = self.repairs_db.execute(query)
        repairs = []
        for row in result:
            repairs.append(repair_from_row(row))
        return repairs

    def create_repair(self, repair):
        repair.validate()
        query = add_repair_query(repair.start_date,
                                 repair.end_date,
                                 repair.is_completed,
                                 repair.propose_complete,
                                 repair.assigned_user_id)
        result = self.repairs_db.execute(query)
        return result.lastrowid

    def get_repair_by_id(self, repair_id):
        query = get_repair_by_id_query(repair_id)
        result = self.repairs_db.execute(query)
        row = result.fetchone()
        result.close()
        if row is None:
            raise RepairNotFoundException(repair_id)
        return repair_from_row(row)

    def delete_repair_by_id(self, repair_id):
        query = delete_repair_by_id_query(repair_id)
        result = self.repairs_db.execute(query)
        if result.rowcount != 1:
            raise RepairNotFoundException(repair_id)

    def propose_repair_completion(self, repair_id):
        query = propose_repair_completion_query(repair_id)
        result = self.repairs_db.execute(query)
        if result.rowcount != 1:
            raise RepairNotFoundException(repair_id)

    def mark_repair_completed(self, repair_id):
        query = mark_repair_completed_query(repair_id)
        result = self.repairs_db.execute(query)
        if result.rowcount != 1:
            raise RepairNotFoundException(repair_id)

    def update_repair(self, repair):
        query = update_repair_by_id_query(repair)
        result = self.repairs_db.execute(query)
        if result.rowcount != 1:
            raise RepairNotFoundException(repair.repair_id)

    def get_repair_comments(self, repair_id):
        self.get_repair_by_id(repair_id)  # to verify if it exists
        query = get_repair_comments_query(repair_id)
        result = self.repairs_db.execute(query)
        comments = []
        for row in result:
            comments.append(CommentSchema().load(CommentSchema().dump(row).data).data)
        return comments

    def add_comment(self, comment):
        if self.get_repair_by_id(comment.repair_id) is None:
            raise RepairNotFoundException(comment.repair_id)
        query = add_comment_query(comment)
        result = self.repairs_db.execute(query)
        if result.rowcount != 1:
            raise CommentPostFailedException()
