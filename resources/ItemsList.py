from flask_restful import Resource
from items import items


class ItemsList(Resource):

    def get(self):
        return {'items': items}, 200