from .engine import SessionLocal


def get_database_session():
    try:
        db_session = SessionLocal()
        return db_session
    except Exception as e:
        print(f"Error creating database session: {e}")
        return False
