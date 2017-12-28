from flask import Flask
from flask_restful import Api

from app.DependencyInjector import DependencyInjector
from app.restful.RegisterResource import RegisterResource
from app.restful.RepairDetailsResources import RepairDetailsResource, RepairProposeCompletionResource, \
    RepairMarkCompetedResource, RepairCommentsResource
from app.restful.RepairsResource import RepairsResource
from app.restful.Resources import USE_CASE_FACTORY
from app.restful.LoginResource import LoginResource
from app.restful.UsersResources import UsersResource, UserDetailsResource, SearchUsersResource


class App:
    def __init__(self, db_url):
        print('name: ' + __name__)
        self.__di = DependencyInjector(db_url)
        self.flaskApp = Flask(__name__)
        self.api = Api(self.flaskApp)

    def init(self):
        self.__init_restful()
        return self.flaskApp

    def __init_restful(self):
        self.__add_resource(LoginResource, '/auth/login')
        self.__add_resource(RegisterResource, '/auth/register')
        self.__add_resource(RepairsResource, '/repairs')
        self.__add_resource(RepairDetailsResource, '/repairs/<repair_id>')
        self.__add_resource(RepairProposeCompletionResource, '/repairs/<repair_id>/proposeComplete')
        self.__add_resource(RepairMarkCompetedResource, '/repairs/<repair_id>/markCompleted')
        self.__add_resource(RepairCommentsResource, '/repairs/<repair_id>/comments')
        self.__add_resource(UsersResource, '/users')
        self.__add_resource(UserDetailsResource, '/users/<username>')
        self.__add_resource(SearchUsersResource, '/users/search')

    def __add_resource(self, resource_class, path):
        self.api.add_resource(resource_class, path, resource_class_kwargs={
            USE_CASE_FACTORY: self.__di.provide_use_case_factory()
        })
