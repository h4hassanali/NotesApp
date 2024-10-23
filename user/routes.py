from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status, BackgroundTasks
from user.service import create_user, validate_credentials, check_user, get_access_token
from user.logging import log_user_action
from .schemas import (
    UserSignupRequest,
    UserSigninRequest,
    UserSigninResponse,
)

user_router = APIRouter()


@user_router.post("/signup", response_model = UserSigninResponse, status_code = status.HTTP_201_CREATED)
def signup(user_data: UserSignupRequest, background_task: BackgroundTasks):
    if check_user(email = user_data.email):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this email already exists"
        )

    new_user = create_user(user_data)
    access_token = get_access_token(new_user)
    background_task.add_task(log_user_action, new_user.id, "signUp")

    return access_token


@user_router.post("/signin", response_model = UserSigninResponse, status_code = status.HTTP_200_OK)
def signin(background_task: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends(), ):
    user_data = UserSigninRequest(email = form_data.username, password = form_data.password)
    user = validate_credentials(user_data)
    if user:
        access_token = get_access_token(user)
        background_task.add_task(log_user_action, user.id, "siginIn")
        return access_token
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Invalid Email or Password"
    )
