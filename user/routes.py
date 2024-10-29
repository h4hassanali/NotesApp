from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from user.service import create_user, get_access_token
from user.common_services import check_user
from common_services.logging import log_user_action
from user.schemas import SignupRequest
from auth.schemas import SigninResponse

user_router = APIRouter()


@user_router.post("/signup", response_model = SigninResponse, status_code = status.HTTP_201_CREATED)
def signup(user_data: SignupRequest, background_task: BackgroundTasks):
    if check_user(email = user_data.email):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this email already exists"
        )

    new_user = create_user(user_data)
    access_token = get_access_token(new_user)
    background_task.add_task(log_user_action, new_user.id, "signUp")

    return access_token