import jwt
import datetime
from flask import current_app
from abc import ABC, abstractmethod


class Token(ABC):
    @abstractmethod
    def get_token_str(self):
        pass


class JWTToken(Token):
    def __init__(self, payload, secret_key):
        self._payload = payload
        self._secret_key = secret_key

    def get_token_str(self):
        return jwt.encode(self._payload, self._secret_key, algorithm='HS256')


class TokenFactory(ABC):
    @abstractmethod
    def create_token(self, username):
        pass


class JWTTokenFactory(TokenFactory):
    def create_token(self, username):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return JWTToken(payload, current_app.config['SECRET_KEY'])


def generate_token(username):
    token_factory = JWTTokenFactory()
    token = token_factory.create_token(username)
    return token.get_token_str()


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
