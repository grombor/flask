from resources.User import User
from hmac import compare_digest


users = [
    User(1, 'admin', '1234a')
]


username_mapping = {u.username: u for u in users}

usersid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return usersid_mapping.get(user_id, None)