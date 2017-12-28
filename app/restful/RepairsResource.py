from flask import request

from app.restful.Resources import ApiAuthenticatedResource, errorResponse, successResponse
from domain.Exceptions import ApiException
from domain.entities.Repair import Repair, RepairSchema
from sql_queries import COLUMN_START_DATE, COLUMN_END_DATE, COLUMN_IS_COMPLETED, COLUMN_PROPOSE_COMPLETE, \
    COLUMN_ASSIGNED_USER


class RepairsResource(ApiAuthenticatedResource):
    def get(self, **kwargs):
        from_inclusive = request.args['from']
        to_exclusive = request.args['to']
        result = self.use_case_factory.get_repairs_list_use_case(from_inclusive, to_exclusive).execute()
        json = [RepairSchema().dump(r)[0] for r in result]
        return successResponse(json)

    def put(self, **kwargs):
        data = request.get_json(force=True)
        try:
            result = self.use_case_factory.create_repair_use_case(
                Repair(
                    None,
                    data[COLUMN_START_DATE],
                    data[COLUMN_END_DATE],
                    data[COLUMN_IS_COMPLETED],
                    data[COLUMN_PROPOSE_COMPLETE],
                    data[COLUMN_ASSIGNED_USER]
                )).execute()
        except ApiException as error:
            return errorResponse(error)
        return successResponse({"repair_id": result})
