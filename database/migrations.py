# database_migrations.py
from database.engine import engine
from user.models import User
from note.models import Note


# Create tables for User and Note models
def migrate():
    User.__table__.create(bind=engine, checkfirst=True)
    Note.__table__.create(bind=engine, checkfirst=True)
    print("Database tables created successfully.")
