import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from hmac import compare_digest

class User:

    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password


    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM  users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
           user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user


    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM  users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
           user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
    'username',
    type = str,
    required = True,
    help = "This field cannot be empty!"
    )
    parser.add_argument(
    'password',
    type = str,
    required = True,
    help = "This field cannot be empty!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created.'}, 200


class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
    'username',
    type = str,
    required = True,
    help = "This field cannot be empty!"
    )
    parser.add_argument(
    'password',
    type = str,
    required = True,
    help = "This field cannot be empty!"
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        user = User.find_by_username(data['username'])
        if user and compare_digest(data['password'], user.password):
            token = create_access_token(identity=user.id)
            return {'token': token}, 200
        else:
            return {'message': 'Wrong user login or password.'}, 400
