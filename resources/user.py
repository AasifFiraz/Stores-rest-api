import datetime

from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from blacklist import BLACKLIST
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    jwt_refresh_token_required, jwt_required, get_raw_jwt)

# Underscore means u can't import this from another file
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="field cannot be blank"
                          )

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="field cannot be blank"
                          )


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists with similar username"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "user created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': "user deleted"}
        else:
            return {"message": "user not found"}, 404


class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()

        # This is what the authenticate function used to do in security.py
        user = UserModel.find_by_username(data["username"])
        if user and compare_digest(user.password, data['password']):
            # Identity - This is what the identity function used to do in security.py
            expires = datetime.timedelta(days=2)
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {'message': "Successfully Logged out"}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
