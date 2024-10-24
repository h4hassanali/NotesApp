import logging
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, Request, status, BackgroundTasks
from auth.service import exchange_code_for_token, get_user_info
from user.service import create_user, get_user_by_email, validate_credentials, check_user, get_access_token
from user.logging import log_user_action
from .schemas import (
    UserSignupRequest,
    UserSigninRequest,
    UserSigninResponse,
    UserSignupResponse,
)
from fastapi.security import oauth2
import requests
from configuration import Config

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


@user_router.get("/login/google")
async def login_google():
    google_oauth_url = (
        f"{Config.get_env_variable('GOOGLE_OAUTH_URL')}?"
        f"response_type=code&client_id={Config.get_env_variable('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={Config.get_env_variable('GOOGLE_REDIRECT_URI')}"
        "&scope=openid%20profile%20email&access_type=offline"
    )
    return {"url": google_oauth_url}


@user_router.get("/auth/google/callback", response_model=UserSigninResponse)
async def auth_google_callback(code: str, background_task: BackgroundTasks):
    access_token = await exchange_code_for_token(code)
    user_info = await get_user_info(access_token)

    email = user_info.get("email")
    user = get_user_by_email(email=email)

    if not user:
        user = create_user(UserSignupRequest(
            name=user_info.get("name"),
            email=email,
            password=""
        ))

    token_data = get_access_token(user)
    background_task.add_task(log_user_action, user.id, "googleSignIn")

    return UserSigninResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        user=UserSignupResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )
