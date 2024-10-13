from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from database.session import get_database_session
from .schemas import (
    UserSignupRequest,
    UserSignupResponse,  
    UserSigninRequest,
    UserSigninResponse,
)

user_router = APIRouter()


# Signup route
@user_router.post(
    "/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED
)
def signup(user_data: UserSignupRequest, db: Session = Depends(get_database_session)):
    # Check if user already exists
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create a new user
    new_user = User(
        name=user_data.name, email=user_data.email, password=user_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Signin route
@user_router.post(
    "/signin", response_model=UserSigninResponse, status_code=status.HTTP_200_OK
)
def signin(user_data: UserSigninRequest, db: Session = Depends(get_database_session)):
    # Validate user credentials
    user = (
        db.query(User)
        .filter(User.email == user_data.email, User.password == user_data.password)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password"
        )

    return user
