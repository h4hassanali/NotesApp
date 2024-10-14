# services/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from user.models import User
from user.schemas import UserSignupRequest, UserSigninRequest


def service_to_create_user(user_data: UserSignupRequest, database: Session):
    new_user = User(
        name=user_data.name, email=user_data.email, password=user_data.password
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


def service_to_validate_user_credentials(
    user_data: UserSigninRequest, database: Session
):
    user = (
        database.query(User)
        .filter(
            User.email == user_data.email, User.password == user_data.password
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password",
        )
    return user
