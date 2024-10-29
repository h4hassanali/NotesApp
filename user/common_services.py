from pydantic import EmailStr
from sqlalchemy.orm import Session
from database.service import get_database_session
from user.models import User
from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utils.configuration import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_id = extract_id_from_token(token = token)
        if user_id is None:
            return None
        user = get_user_by_id(int(user_id))
        if user is None:
            return None
        return user
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None


def extract_id_from_token(token: str):
    payload = jwt.decode(token, Config.get_env_variable("SECRET_KEY"), algorithms=[Config.get_env_variable("ALGORITHM")])
    user_id = payload.get("sub")
    return user_id


def get_user_by_id(user_id: int):
    with get_database_session() as database:
        return database.query(User).filter(User.id == user_id).first()
    

def get_user_by_email(email: EmailStr):
    with get_database_session() as database:
        return database.query(User).filter(User.email == email).first()


def check_user(email: EmailStr = None, user_id: int = None):
    with get_database_session() as database:
        return user_exists(database, email = email, user_id = user_id)


def user_exists(database: Session, email: EmailStr = None, user_id: int = None):
    query = database.query(User)
    if email:
        return query.filter(User.email == email).first() is not None
    if user_id:
        return query.filter(User.id == user_id).first() is not None
    return False
