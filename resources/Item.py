from flask import request
from flask_restful import Resource, reqparse
from pkg_resources import require
from items import items
from flask_jwt_extended import jwt_required


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field cannot be empty!"
    )


    def find_by_name(self, name) -> None:
        for item in items:
            if item["name"] == name:
                return item
        return None


    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        return ({'item': item}, 200) if item else ({'item': None}, 404)


    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f"An item with name {name} already exists."}, 400
        data = Item.parser.parse_args()
        item = {'name': name,'price': data['price']}
        items.append(item)
        return item, 201


    @jwt_required()
    def delete(self, name):
        global items
        item = self.find_by_name(name)
        if item:
            items.remove(item)
            return {'message': 'Item deleted successfully.'}, 200
        return {'message': f'Cannot delete item with name {name}'}, 400


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        if item is None:
            item = {'name': name, 'price': data['price']}
            global items
            items.append(item)
        else:
            item.update(data)
        return item, 200