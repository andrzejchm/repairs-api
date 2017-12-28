from domain.usecases.UseCase import UseCase


class DeleteUserByIdUseCase(UseCase):
    def __init__(self, users_entity_gateway, username):
        self.users_entity_gateway = users_entity_gateway
        self.username = username

    def execute(self):
        return self.users_entity_gateway.delete_user(self.username)
