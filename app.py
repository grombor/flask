from flask import Flask, request
from flask_restful import Api

from resources.Item import Item
from resources.ItemsList import ItemsList
from resources.User import UserRegister, UserLogin
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    app.run(debug=True)

