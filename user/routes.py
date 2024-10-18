from fastapi import APIRouter, HTTPException, status
from user.service import (
    create_user,
    validate_credentials,
)
from .schemas import (
    UserSignupRequest,
    UserSignupResponse,
    UserSigninRequest,
    UserSigninResponse,
)
from user.service import check_user

user_router = APIRouter()


@user_router.post("/signup", response_model = UserSignupResponse, status_code = status.HTTP_201_CREATED)
def signup(user_data: UserSignupRequest):
    user_exist = check_user(email = user_data.email)
    if not user_exist:
        new_user = create_user(user_data)
        return new_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User Already Exists",
    )    


@user_router.post("/signin", response_model = UserSigninResponse, status_code = status.HTTP_200_OK)
def signin(user_data: UserSigninRequest):
    user = validate_credentials(user_data)
    if user:
        return user
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Invalid Email or Password",
    )
