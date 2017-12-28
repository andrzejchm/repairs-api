import jwt
import datetime
from config import SECRET_KEY, JWT_ALGORITHM, TOKEN_EXPIRATION_SECONDS

JWT_TIMESTAMP_KEY = 'timestamp'
JWT_USER_ROLE = 'role'
JWT_IDENTITY_KEY = 'identity'


def create_jwt_token(user):
    timestamp = datetime.datetime.now().timestamp() + TOKEN_EXPIRATION_SECONDS
    jwt_object = {JWT_IDENTITY_KEY: user.username, JWT_TIMESTAMP_KEY: timestamp, JWT_USER_ROLE: user.role}
    jwt_token = jwt.encode(jwt_object, SECRET_KEY, algorithm=JWT_ALGORITHM).decode('utf-8')
    return jwt_token


def parse_jwt_token(jwt_token):
    jwt_contents = jwt.decode(jwt_token, SECRET_KEY, algorithm=JWT_ALGORITHM)
    username = jwt_contents[JWT_IDENTITY_KEY]
    timestamp = jwt_contents[JWT_TIMESTAMP_KEY]
    role =  jwt_contents[JWT_USER_ROLE]
    return username, timestamp, role
