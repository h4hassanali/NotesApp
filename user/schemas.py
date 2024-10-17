from pydantic import BaseModel, EmailStr


class UserSignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserSignupResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSigninRequest(BaseModel):
    email: EmailStr
    password: str


class UserSigninResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
