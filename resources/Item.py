from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import sqlite3


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument(
    'price',
    type = float,
    required = True,
    help = "This field cannot be empty!"
    )


    @classmethod
    def find_by_name(cls, name) -> None:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM  items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
           item = cls(*row)
        else:
            item = None
        
        connection.close()
        return item


    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}, 404


    @classmethod
    def insert(cls, item):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    
    @classmethod
    def update(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item, 201


    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted. '}, 200


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occured inserting the item.'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occured updated the item.'}, 500

        return updated_item