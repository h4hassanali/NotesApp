from fastapi import APIRouter, HTTPException, status
from user.service import (
    create_user_service,
    validate_credentials_service,
)
from .schemas import (
    UserSignupRequest,
    UserSignupResponse,
    UserSigninRequest,
    UserSigninResponse,
)
from user.service import check_user_service

user_router = APIRouter()


@user_router.post("/signup", response_model = UserSignupResponse, status_code = status.HTTP_201_CREATED)
def signup(user_data: UserSignupRequest):
    if not check_user_service(email = user_data.email):
        new_user = create_user_service(user_data)
        return new_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User Already Exists",
    )    


@user_router.post("/signin", response_model = UserSigninResponse, status_code = status.HTTP_200_OK)
def signin(user_data: UserSigninRequest):
    user = validate_credentials_service(user_data)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password",
    )
