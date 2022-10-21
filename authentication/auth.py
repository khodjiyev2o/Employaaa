from xmlrpc.client import Boolean
import jwt
from fastapi import HTTPException, Security, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os 
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from .utils import VerifyToken
from database.database import database
from database.models import users




token_auth_scheme = HTTPBearer()

load_dotenv()

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.environ.get("SECRET")

    def get_password_hash(self, password)->str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password)->Boolean:
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, email)->str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token:str,response=Response):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            try:
               result = VerifyToken(token.credentials).verify()
               if result.get("status"):
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return result
               return result
            except:
                raise HTTPException(status_code=401, detail='Invalid token')
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security))->users.c.email:
        return self.decode_token(auth.credentials)

    def get_current_user(self,auth: HTTPAuthorizationCredentials = Security(security))->users.c.email:
        user_email = self.decode_token(auth.credentials)
        return user_email

