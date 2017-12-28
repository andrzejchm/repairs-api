from abc import ABC, abstractmethod


class UserEntityGateway(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def create_user(self, user_id, password):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def search_users(self, query):
        pass


    @abstractmethod
    def delete_user(self, username):
        pass
