from pydantic import BaseModel, EmailStr
from user.schemas import SignupResponse


class SigninRequest(BaseModel):
    email: EmailStr
    password: str


class SigninResponse(BaseModel):
    access_token: str
    token_type: str
    user: SignupResponse

    class Config:
        orm_mode = True
