# services/user_service.py
from user.models import User
from user.schemas import UserSignupRequest, UserSigninRequest
from database.service import get_database_session
from pydantic import EmailStr


def create_user_service(user_data: UserSignupRequest):
    database = get_database_session()
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = user_data.password,
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    database.close()

    return new_user
        

def validate_credentials_service(user_data: UserSigninRequest):
    database = get_database_session()
    user = (
        database.query(User)
        .filter(User.email == user_data.email,User.password == user_data.password).first()
    )
    database.close()
    if not user:
        return False
    return user


def check_user_service(email: EmailStr = None, user_id: int = None):
    database = get_database_session()
    try:
        if email:
            if check_email_registered(database, email):
                return True
        elif user_id is not None:
            if check_user_exists(database, user_id):
                return True
        return False
    finally:
        database.close()


def check_email_registered(database, email: EmailStr):
    user = database.query(User).filter(User.email == email).first()
    if user:
        return True
    return False


def check_user_exists(database, user_id: int):
    user = database.query(User).filter(User.id == user_id).first()
    if user:
        return True
    return False
