from marshmallow import Schema, fields, post_load

from config import REPAIR_DURATION_SECONDS
from domain.Exceptions import InvalidDateRangeException, InvalidRepairDurationException


class Repair:
    def __init__(self, repair_id, start_date, end_date, is_completed, propose_complete, assigned_user_id):
        self.repair_id = repair_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_completed = is_completed
        self.propose_complete = propose_complete
        self.assigned_user_id = assigned_user_id

    def validate(self):
        if self.start_date > self.end_date:
            raise InvalidDateRangeException(self.start_date, self.end_date)
        if self.end_date - self.start_date != REPAIR_DURATION_SECONDS:
            raise InvalidRepairDurationException(self.end_date - self.start_date)


class RepairSchema(Schema):
    repair_id = fields.Integer(load_from="id", dump_to="id", required=False)
    start_date = fields.Integer(load_from="startDate", dump_to="startDate", required=True, validate=lambda x: x >= 0)
    end_date = fields.Integer(load_from="endDate", dump_to="endDate", required=True, validate=lambda x: x >= 0)
    is_completed = fields.Boolean(load_from="isCompleted", dump_to="isCompleted", required=True)
    propose_complete = fields.Boolean(load_from="proposeComplete", dump_to="proposeComplete", required=True)
    assigned_user_id = fields.Str(load_from="assignedUser", dump_to="assignedUser", required=True)

    @post_load
    def make_repair(self, data):
        return Repair(**data)
