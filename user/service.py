# services/user_service.py

from user.models import User
from user.schemas import UserSignupRequest, UserSigninRequest
from database.service import get_database_session
from pydantic import EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user_data: UserSignupRequest) -> User:
    with get_database_session() as database:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=get_password_hash(user_data.password),
        )
        database.add(new_user)
        database.commit()
        database.refresh(new_user)

    return new_user


def validate_credentials(user_data: UserSigninRequest) -> User | bool:
    with get_database_session() as database:
        user = database.query(User).filter(
            User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password):
        return False

    return user


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def check_user(email: EmailStr = None, user_id: int = None) -> bool:
    with get_database_session() as database:
        if email:
            return user_exists(database, email=email)
        elif user_id:
            return user_exists(database, user_id=user_id)

    return False


def user_exists(database: Session, email: EmailStr = None, user_id: int = None) -> bool:
    query = database.query(User)
    if email:
        return query.filter(User.email == email).first() is not None
    elif user_id:
        return query.filter(User.id == user_id).first() is not None
    return False
