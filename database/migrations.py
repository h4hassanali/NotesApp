# database_migrations.py
from database.engine import engine
from user.models import User
from note.models import Note
from sqlalchemy.exc import SQLAlchemyError


# Create tables for User and Note models
def migrate():
    try:
        User.__table__.create(bind=engine, checkfirst=True)
        Note.__table__.create(bind=engine, checkfirst=True)
        print("Database tables created successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred while creating tables: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
