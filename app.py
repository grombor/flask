from flask import Flask
from flask_restful import Api

from resources.Item import Item
from resources.ItemsList import ItemsList


app = Flask(__name__)
api = Api(app)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

if __name__ == '__main__':
    app.run(debug=True)

