# services/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from user.models import User
from user.schemas import UserSignupRequest, UserSigninRequest
from database.dependencies import get_database_session


def create_user(user_data: UserSignupRequest):
    database = get_database_session()
    try:
        new_user = User(
            name = user_data.name,
            email = user_data.email,
            password = user_data.password,
        )
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
    except SQLAlchemyError as e:
        database.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Could not create user: {}".format(str(e)),
        )
    finally:
        database.close()
    return new_user


def validate_user_credentials(user_data: UserSigninRequest):
    database = get_database_session()
    try:
        user = (
            database.query(User)
            .filter(
                User.email == user_data.email,
                User.password == user_data.password,
            )
            .first()
        )
        if not user:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Invalid email or password",
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Database error: {}".format(str(e)),
        )
    finally:
        database.close()
    return user
