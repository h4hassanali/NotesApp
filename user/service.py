from datetime import timedelta
from auth.service import create_access_token, get_password_hash, verify_password
from user.common_services import get_user_by_email
from user.models import User
from user.schemas import SignupRequest
from auth.schemas import SigninRequest
from database.service import get_database_session
from configuration import Config

def create_user(user_data: SignupRequest):
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
        expires_delta = timedelta(minutes = int(Config.get_env_variable('ACCESS_TOKEN_EXPIRE_MINUTES')))
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


def validate_credentials(user_data: SigninRequest):
    user = get_user_by_email(user_data.email)
    if user and verify_password(user_data.password, user.password):
        return user
    return False