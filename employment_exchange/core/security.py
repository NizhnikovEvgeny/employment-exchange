from passlib.context import CryptContext
from jose import jwt
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ENCODE_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(user_data: dict) -> str:
    to_encode = user_data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() +
                     datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, ENCODE_ALGORITHM)


def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(
            token, SECRET_KEY, algorithms=ENCODE_ALGORITHM)
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
        return await super().__call__(request)
