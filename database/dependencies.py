# database/dependencies.py
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from .engine import SessionLocal


def get_database_session():
    try:
        db_session = SessionLocal()
        return db_session
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Database connection error: {}".format(str(e)),
        )
