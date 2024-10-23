from datetime import datetime, timedelta, timezone
from jose import jwt
from configuration import Config
from passlib.context import CryptContext

SECRET_KEY = Config.get_env_variable('SECRET_KEY')
ALGORITHM = Config.get_env_variable('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = Config.get_env_variable('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.now(
        timezone.utc) + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))
    data_to_encode = {**data, "exp": expire, "sub": str(data.get("sub"))}
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm = ALGORITHM)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
