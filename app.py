from flask import Flask, request
from flask_restful import Api

from resources.Item import Item
from resources.ItemsList import ItemsList
from users import authenticate

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if authenticate(username, password):
        access_token = create_access_token(identity=username)
        return access_token

if __name__ == '__main__':
    app.run(debug=True)

