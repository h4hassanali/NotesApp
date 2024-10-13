from .engine import SessionLocal


def get_database_session():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
