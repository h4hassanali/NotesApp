# initialize_tables.py
from database.db import engine
from user.models import User
from note.models import Note


# Create tables for User and Note models
def initialize_tables():
    # Create all tables in the database
    User.__table__.create(bind=engine, checkfirst=True)
    Note.__table__.create(bind=engine, checkfirst=True)
    print("Database tables created successfully.")
