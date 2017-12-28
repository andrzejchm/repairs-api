from domain.usecases.CreateRepairUseCase import CreateRepairUseCase
from domain.usecases.DeleteRepairByIdUseCase import DeleteRepairByIdUseCase
from domain.usecases.DeleteUserByIdUseCase import DeleteUserByIdUseCase
from domain.usecases.GetRepairByIdUseCase import GetRepairByIdUseCase
from domain.usecases.GetRepairCommentsUseCase import GetRepairCommentsUseCase
from domain.usecases.GetRepairsListUseCase import GetRepairsListUseCase
from domain.usecases.GetUserDetailsUseCase import GetUserDetailsUseCase
from domain.usecases.GetUsersUseCase import GetUsersUseCase
from domain.usecases.LogInUseCase import LogInUseCase
from domain.usecases.MarkRepairCompletedUseCase import MarkRepairCompletedUseCase
from domain.usecases.PostCommentUseCase import PostCommentUseCase
from domain.usecases.ProposeRepairCompletionUseCase import ProposeRepairCompletionUseCase
from domain.usecases.RegisterUserUseCase import RegisterUserUseCase
from domain.usecases.SearchUsersUseCase import SearchUsersUseCase
from domain.usecases.UpdateRepairUseCase import UpdateRepairUseCase


class UseCaseFactory:
    def __init__(self, users_entity_gateway, repairs_entity_gateway):
        self.users_entity_gateway = users_entity_gateway
        self.repairs_entity_gateway = repairs_entity_gateway

    def log_in_use_case(self, username, password_hash):
        return LogInUseCase(self.users_entity_gateway, username, password_hash)

    def register_user_use_case(self, username, password):
        return RegisterUserUseCase(self.users_entity_gateway, username, password)

    def get_repairs_list_use_case(self, from_timestamp_inclusive, to_timestamp_exclusive):
        return GetRepairsListUseCase(self.repairs_entity_gateway, from_timestamp_inclusive, to_timestamp_exclusive)

    def create_repair_use_case(self, repair):
        return CreateRepairUseCase(self.repairs_entity_gateway, repair)

    def get_repair_by_id_use_case(self, repair_id):
        return GetRepairByIdUseCase(self.repairs_entity_gateway, repair_id)

    def delete_repair_by_id_use_case(self, repair_id):
        return DeleteRepairByIdUseCase(self.repairs_entity_gateway, repair_id)

    def propose_repair_completion_use_case(self, repair_id):
        return ProposeRepairCompletionUseCase(self.repairs_entity_gateway, repair_id)

    def mark_repair_completed_use_case(self, repair_id):
        return MarkRepairCompletedUseCase(self.repairs_entity_gateway, repair_id)

    def update_repair_use_case(self, repair):
        return UpdateRepairUseCase(self.repairs_entity_gateway, repair)

    def get_repair_comments_use_case(self, repair_id):
        return GetRepairCommentsUseCase(self.repairs_entity_gateway, repair_id)

    def post_comment_use_case(self, comment):
        return PostCommentUseCase(self.repairs_entity_gateway, comment)

    def get_users_use_case(self):
        return GetUsersUseCase(self.users_entity_gateway)

    def get_user_details_use_case(self, username):
        return GetUserDetailsUseCase(self.users_entity_gateway, username)

    def search_users_use_case(self, query):
        return SearchUsersUseCase(self.users_entity_gateway, query)

    def delete_user_by_id_use_case(self, username):
        return DeleteUserByIdUseCase(self.users_entity_gateway, username)
