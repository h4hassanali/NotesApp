from fastapi import APIRouter, Depends, status
from user.service import (
    service_to_create_user,
    service_to_validate_user_credentials,
)
from user.utils import check_user
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
def signup(user_data: UserSignupRequest):

    check_user(email=user_data.email)

    new_user = service_to_create_user(user_data)

    return new_user


# Signin route
@user_router.post(
    "/signin",
    response_model=UserSigninResponse,
    status_code=status.HTTP_200_OK,
)
def signin(user_data: UserSigninRequest):
    user = service_to_validate_user_credentials(user_data)

    return user
