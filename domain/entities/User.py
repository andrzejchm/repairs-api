from marshmallow import fields, Schema, post_load

DEFAULT_USER_ROLE = 'user'
MANAGER_USER_ROLE = 'manager'
ADMIN_USER_ROLE = 'admin'

USER_ROLES_HIERARCHY = {
    DEFAULT_USER_ROLE: 0,
    MANAGER_USER_ROLE: 1,
    ADMIN_USER_ROLE: 2
}


class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def isAtLeastManager(self):
        return USER_ROLES_HIERARCHY[self.role] >= USER_ROLES_HIERARCHY[MANAGER_USER_ROLE]


class RegisterUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class LogInUser:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


class UserSchema(Schema):
    username = fields.Str(load_from="username", dump_to="username", required=True)
    password_hash = fields.Str(load_from="passwordHash", dump_to="passwordHash", required=True)
    role = fields.Str(load_from="role", dump_to="role", required=True)

    @post_load
    def make_user(self, data):
        return User(**data)


class GetUserSchema(Schema):
    username = fields.Str(load_from="username", dump_to="username", required=True)
    role = fields.Str(load_from="role", dump_to="role", required=True)

    @post_load
    def make_user(self, data):
        return User(password_hash=None, **data)


class LogInUserSchema(Schema):
    username = fields.Str(load_from="username", dump_to="username", required=True)
    password_hash = fields.Str(load_from="passwordHash", dump_to="passwordHash", required=True)

    @post_load
    def make_user(self, data):
        return LogInUser(**data)


class RegisterUserSchema(Schema):
    username = fields.Str(load_from="username", dump_to="username", required=True)
    password = fields.Str(load_from="password", dump_to="password", required=True)

    @post_load
    def make_register_user(self, data):
        return RegisterUser(**data)
