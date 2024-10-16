from fastapi import HTTPException, status
from user.models import User
from database.dependencies import get_database_session
from pydantic import EmailStr


def check_email_registered(database, email: EmailStr):
    user = database.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered",
        )


def check_user_exists(database, user_id: int):
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail = "User not found"
        )


def check_user(email: EmailStr = None, user_id: int = None):
    database = get_database_session()
    try:
        if email:
            check_email_registered(database, email)
        elif user_id is not None:
            check_user_exists(database, user_id)
        else:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Either email or user ID must be provided",
            )
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred: {}".format(str(e)),
        )
    finally:
        database.close()

    return None
