from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.store import Store, StoreList
from resources.item import Item, ItemList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "n3bo2i3eiofb2b1cs"  # app.config
api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


jwt_token = JWTManager(app=app)  # does not create /auth, we have to do manually


@jwt_token.expired_token_loader
def expired_token_callback():
    return jsonify({"description": "Token is expired", "error": "expired token"})


# When the user enters an invalid jwt token
@jwt_token.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"description": "Signature verification failed", "error": "invalid token"}), 401


# When JWT token is not passed in the header
@jwt_token.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"description": "Request does not contain an access token", "error": "no token"})


@jwt_token.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({"description": "Please login with your credentials and pass the access token",
                    "error": "fresh token required"})


@jwt_token.revoked_token_loader
def revoked_token_callback():
    return jsonify({"description": "The token has been revoked", "error": "revoked_token"})


api.add_resource(Item, '/item/<string:name>')  # same as @app.route("/item/<string:name>")
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
