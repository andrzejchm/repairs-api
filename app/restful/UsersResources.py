from flask import request

from app.restful.Resources import ApiAuthenticatedResource, errorResponse, successResponse, get_user
from domain.Exceptions import ApiException, MustBeAtLeastManagerException, CannotDeleteYourselfException
from domain.entities.Repair import Repair, RepairSchema
from domain.entities.User import UserSchema, GetUserSchema
from sql_queries import COLUMN_START_DATE, COLUMN_END_DATE, COLUMN_IS_COMPLETED, COLUMN_PROPOSE_COMPLETE, \
    COLUMN_ASSIGNED_USER


class UsersResource(ApiAuthenticatedResource):
    def get(self, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            result = self.use_case_factory.get_users_use_case().execute()
            json = [GetUserSchema().dump(user).data for user in result]
            return successResponse(json)
        except ApiException as ex:
            return errorResponse(ex)


class UserDetailsResource(ApiAuthenticatedResource):
    def get(self, username, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            user = self.use_case_factory.get_user_details_use_case(username).execute()
            json = GetUserSchema().dump(user).data
            return successResponse(json)
        except ApiException as ex:
            return errorResponse(ex)

    def delete(self, username, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            if get_user(**kwargs).username == username.strip():
                raise CannotDeleteYourselfException()
            self.use_case_factory.delete_user_by_id_use_case(username).execute()
            return successResponse("OK")
        except ApiException as ex:
            return errorResponse(ex)


class SearchUsersResource(ApiAuthenticatedResource):
    def get(self, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            query = request.args['q']
            result = self.use_case_factory.search_users_use_case(query).execute()
            json = [GetUserSchema().dump(user).data for user in result]
            return successResponse(json)
        except ApiException as ex:
            return errorResponse(ex)
