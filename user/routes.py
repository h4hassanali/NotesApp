from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.user_services import (
    service_to_create_user,
    service_to_validate_user_credentials,
)
from .models import User
from user.utils import check_user
from database.dependencies import get_database_session
from .schemas import (
    UserSignupRequest,
    UserSignupResponse,
    UserSigninRequest,
    UserSigninResponse,
)

user_router = APIRouter()


@user_router.post(
    "/signup",
    response_model=UserSignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    user_data: UserSignupRequest,
    database: Session = Depends(get_database_session),
):

    check_user(email=user_data.email, database=database)

    new_user = service_to_create_user(user_data, database)

    return new_user


# Signin route
@user_router.post(
    "/signin",
    response_model=UserSigninResponse,
    status_code=status.HTTP_200_OK,
)
def signin(
    user_data: UserSigninRequest,
    database: Session = Depends(get_database_session),
):
    # Validate user credentials
    user = service_to_validate_user_credentials(user_data, database)

    return user
