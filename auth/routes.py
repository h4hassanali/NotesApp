from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status, BackgroundTasks
from auth.service import exchange_code_for_token, get_user_info
from user.service import create_user, get_user_by_email, validate_credentials, get_access_token
from auth.logging import log_user_action
from user.schemas import SignupRequest, SignupResponse
from auth.schemas import SigninRequest, SigninResponse
from configuration import Config

auth_router = APIRouter()


@auth_router.post("/signin", response_model = SigninResponse, status_code = status.HTTP_200_OK)
def signin(background_task: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends(), ):
    user_data = SigninRequest(
        email = form_data.username, password = form_data.password)
    user = validate_credentials(user_data)
    if user:
        access_token = get_access_token(user)
        background_task.add_task(log_user_action, user.id, "siginIn")
        return access_token
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Invalid Email or Password"
    )


@auth_router.get("/login/google")
async def login_google():
    google_oauth_url = (
        f"{Config.get_env_variable('GOOGLE_OAUTH_URL')}?"
        f"response_type=code&client_id={Config.get_env_variable('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={Config.get_env_variable('GOOGLE_REDIRECT_URI')}"
        "&scope=openid%20profile%20email&access_type=offline"
    )
    return {"url": google_oauth_url}


@auth_router.get("/google/callback", response_model = SigninResponse)
async def auth_google_callback(code: str, background_task: BackgroundTasks):
    access_token = await exchange_code_for_token(code)
    user_info = await get_user_info(access_token)

    email = user_info.get("email")
    user = get_user_by_email(email = email)

    if not user:
        user = create_user(SignupRequest(
            name = user_info.get("name"),
            email = email,
            password = ""
        ))

    token_data = get_access_token(user)
    background_task.add_task(log_user_action, user.id, "googleSignIn")

    return SigninResponse(
        access_token = token_data["access_token"],
        token_type = token_data["token_type"],
        user = SignupResponse(
            id = user.id,
            name = user.name,
            email = user.email
        )
    )
