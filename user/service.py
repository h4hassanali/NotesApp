from datetime import timedelta
from user.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from user.models import User
from user.schemas import UserSignupRequest, UserSigninRequest
from database.service import get_database_session
from pydantic import EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")


def create_user(user_data: UserSignupRequest):
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = get_password_hash(user_data.password)
    )
    return save_user_to_db(new_user)


def save_user_to_db(user: User):
    with get_database_session() as database:
        database.add(user)
        database.commit()
        database.refresh(user)
    return user


def get_access_token(user: User):
    access_token = create_access_token(
        data = {"sub": str(user.id)},
        expires_delta = timedelta(minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


def validate_credentials(user_data: UserSigninRequest):
    user = get_user_by_email(user_data.email)
    if user and verify_password(user_data.password, user.password):
        return user
    return False


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


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
