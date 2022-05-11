from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "store not found."}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"store {name} already exists"}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "error occurred when creating the store"}, 500

        return store.json(), 201

    def delete(self, name):
        item = StoreModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {"message": f"store '{name}' deleted"}
        else:
            return {"error": f"store '{name}' not found"}


class StoreList(Resource):
    def get(self):
        return {"items": [store.json() for store in StoreModel.find_all()]}
