from pydantic import BaseModel, EmailStr


# Schema for signup request
class UserSignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


# Schema for signup response
class UserSignupResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


# Schema for signin request
class UserSigninRequest(BaseModel):
    email: EmailStr
    password: str


# Schema for signin response
class UserSigninResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
