from fastapi import APIRouter, status
from user.service import (
    create_user,
    validate_user_credentials,
)
from user.utils import check_user
from .schemas import (
    UserSignupRequest,
    UserSignupResponse,
    UserSigninRequest,
    UserSigninResponse,
)

user_router = APIRouter()

@user_router.post("/signup", response_model = UserSignupResponse, status_code = status.HTTP_201_CREATED)
def signup(user_data: UserSignupRequest):
    check_user(email = user_data.email)
    new_user = create_user(user_data)
    return new_user


@user_router.post("/signin", response_model = UserSigninResponse, status_code = status.HTTP_200_OK)
def signin(user_data: UserSigninRequest):
    user = validate_user_credentials(user_data)
    return user
