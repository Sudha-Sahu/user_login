import jwt
from flask import Flask, request
from flask_restful import Api, Resource
from model import User
from mongoengine import connect, ValidationError, NotUniqueError
import json


connect(host='mongodb://127.0.0.1:27017/FlaskUserProject')

app = Flask(__name__)
api = Api(app)


class UserRegisterAPI(Resource):
    def post(self):
        data = json.loads(request.data)
        print('body_data', data)
        user_name = data.get('user_name')
        password = data.get('password')
        conf_password = data.get('conf_password')
        email = data.get('email')
        if conf_password != password:
            return {'error': 'password didnt matched'}
        if not all([user_name, password]):
            return {'error': 'all field are mendatory'}
        try:
            user = User(user_name=user_name, password=password)
            user.save()
            token = jwt.encode({"user_id": user.id, 'user_name': user.user_name}, "deep", algorithm="HS256")
            url = f'http://127.0.0.1:9090/api/user/activate?token={token}'
        except ValidationError as e:
            print(e.to_dict())
            return {'error': e.to_dict()}
        except NotUniqueError as e:
            print(e)
            return {'error': str(e)}
        return {'msg': 'success', 'token_activate_url': url}

    def get(self):
        data = request.args
        user_name = data.get('user_name')
        password = data.get('password')
        print('data get', user_name, password)
        return {'msg': 'success'}


class LoginAPI:
    def get(self):
        data = request.args
        user_name = data.get('user_name')
        password = data.get('password')
        user = User.objects.get(user_name=user_name)
        if not user:
            return {'error': 'user not found'}
        if not user.is_active:
            return {'error': 'You have to verify email'}
        print('password', user.password)
        print('user', user)
        if password != user.password:
            return {'error': 'password not matching'}
        token = jwt.encode({"user_id": user.id, 'user_name': user.user_name}, "deep", algorithm="HS256")
        decode_ = jwt.decode(token, "deep", algorithms=["HS256"])
        print('decoded', decode_)
        print('data get', data.get('user_name'))
        return {'msg': 'success', 'token': token}


class ActivateAccount(Resource):
    def get(self):
        token = request.args.get('token')
        print('token', token)
        decode_ = jwt.decode(token, "deep", algorithms=["HS256"])
        print('decode', decode_)
        user = User.objects.get(id=decode_.get('user_id'))
        user.is_active = True
        user.save()
        return {'msg': 'success'}


api.add_resource(UserRegisterAPI, '/api/user/register')
api.add_resource(ActivateAccount, '/api/user/activate')
api.add_resource(LoginAPI, '/login')

if __name__ == '__main__':
    app.run(debug=True, port=9090)
