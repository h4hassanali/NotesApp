from database.service import get_database_session
from user.models import User
from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from auth.service import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")


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
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    return user_id


def get_user_by_id(user_id: int):
    with get_database_session() as database:
        return database.query(User).filter(User.id == user_id).first()

