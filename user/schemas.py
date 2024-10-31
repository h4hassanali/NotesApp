from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class SignupResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


