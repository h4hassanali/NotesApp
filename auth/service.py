import requests
from fastapi import HTTPException
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


async def exchange_code_for_token(code: str) -> str:
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": Config.get_env_variable('GOOGLE_CLIENT_ID'),
        "client_secret": Config.get_env_variable('GOOGLE_CLIENT_SECRET'),
        "redirect_uri": Config.get_env_variable('GOOGLE_REDIRECT_URI'),
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if "error" in token_json:
        raise HTTPException(
            status_code=400, detail="Failed to fetch token from Google")

    return token_json.get("access_token")


async def get_user_info(access_token: str) -> dict:
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)

    if user_info_response.status_code != 200:
        return False
    return user_info_response.json()
