from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from user.models import User
from pydantic import EmailStr


def check_user(
    email: EmailStr = None, user_id: int = None, database: Session = None
):
    if email:
        user = database.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    elif user_id is not None:
        user = database.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either email or user ID must be provided",
        )
    return None
