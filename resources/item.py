from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel


# With flask restful we don't need jsonify
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="price is needed"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required
    def get(self, name):
        # Using lambda function to return the first data that is called
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 400
        item = ItemModel.find_by_item_name(name)
        if item:
            return item.json()
        else:
            return {"message": "no item found"}

    # By sayying fresh jwt required, it means the token that is retrieved after logging in not refreshing
    @fresh_jwt_required
    def post(self, name):
        # Checking if item is already available using lambda
        # if next(filter(lambda x: x['name'] == name, items), None):
        if ItemModel.find_by_item_name(name):
            return {"message": f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "error occurred when inserting item"}, 500  # Internal server error

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_item_name(name)
        if item:
            # items = list(filter(lambda x: x['name'] != name, items))
            item.delete_from_db()
            return {"message": f"item '{name}' deleted"}
        else:
            return {"error": f"item '{name}' not found"}

    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_item_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"error": "error occurred when inserting the item"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"error": "error occurred when updating the item"}, 500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
