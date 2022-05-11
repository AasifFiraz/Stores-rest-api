import sqlite3
from db import db


class ItemModel(db.Model):
    # Create Table and column in sqlalchemy
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "price": self.price,
                "store_id": self.store_id
                }

    @classmethod
    def find_by_item_name(cls, name):
        # Shortened version using SqlAlchemy
        return cls.query.filter_by(name=name).first()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return cls(row[0], row[1])

    def save_to_db(self):
        # Shortened version using SqlAlchemy
        db.session.add(self)
        db.session.commit()

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price,))
        #
        # connection.commit()
        # connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
