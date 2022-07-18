from flask_restful import Resource
from items import items


class Item(Resource):

    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item, 200
        return {'item': None}, 404

    def post(self, name):
        item = {'name': name,'price': 9.99}
        items.append(item)
        return item, 201