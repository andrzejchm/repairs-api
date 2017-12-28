from flask import request

from app.restful.Resources import ApiAuthenticatedResource, errorResponse, successResponse, errorResponseString, \
    get_user
from domain.Exceptions import ApiException, \
    MustBeAtLeastManagerException, BodyValidationException
from domain.entities.Comment import CommentSchema, PostCommentSchema
from domain.entities.Repair import Repair, RepairSchema


class RepairDetailsResource(ApiAuthenticatedResource):
    def get(self, repair_id, **kwargs):
        try:
            result = self.use_case_factory.get_repair_by_id_use_case(repair_id).execute()
            repair = RepairSchema().dump(result)[0]
            return successResponse(repair)
        except ApiException as ex:
            return errorResponse(ex)

    def post(self, repair_id, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            repair, errors = RepairSchema().load(request.get_json(force=True))
            if errors:
                raise BodyValidationException(errors)
            if int(repair_id) != repair.repair_id:
                return errorResponseString("Path parameter for repair's id does not match body's data", 8)
            repair.repair_id = repair_id
            self.use_case_factory.update_repair_use_case(repair).execute()
            return successResponse("OK")
        except ApiException as ex:
            return errorResponse(ex)

    def delete(self, repair_id, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            self.use_case_factory.delete_repair_by_id_use_case(repair_id).execute()
            return successResponse("OK")
        except ApiException as ex:
            return errorResponse(ex)


class RepairProposeCompletionResource(ApiAuthenticatedResource):
    def post(self, repair_id, **kwargs):
        try:
            self.use_case_factory.propose_repair_completion_use_case(repair_id).execute()
            return successResponse("OK")
        except ApiException as ex:
            return errorResponse(ex)


class RepairMarkCompetedResource(ApiAuthenticatedResource):
    def post(self, repair_id, **kwargs):
        try:
            if not get_user(**kwargs).isAtLeastManager():
                raise MustBeAtLeastManagerException()
            self.use_case_factory.mark_repair_completed_use_case(repair_id).execute()
            return successResponse("OK")
        except ApiException as ex:
            return errorResponse(ex)


class RepairCommentsResource(ApiAuthenticatedResource):
    def get(self, repair_id, **kwargs):
        try:
            result = self.use_case_factory.get_repair_comments_use_case(repair_id).execute()
            comments = CommentSchema(many=True).dump(result)[0]
            return successResponse(comments)
        except ApiException as ex:
            return errorResponse(ex)

    def put(self, repair_id, **kwargs):
        try:
            comment, errors = PostCommentSchema().load(request.get_json(force=True))
            comment.repair_id = int(repair_id)
            if errors:
                raise BodyValidationException(errors)
            self.use_case_factory.post_comment_use_case(comment).execute()
            return successResponse("OK")
        except ApiException as ex:
            return errorResponse(ex)
