from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from note.models import Note
from note.schemas import AddNoteRequest
from database.dependencies import get_database_session


def create_note(note_data: AddNoteRequest):
    database = get_database_session()

    try:
        return create_note_in_db(database, note_data)

    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create note: {}".format(str(e)),
        )

    finally:
        database.close()


def create_note_in_db(database: Session, note_data: AddNoteRequest):
    new_note = Note(
        title = note_data.title,
        content = note_data.content,
        owner_id = note_data.user_id,
    )
    database.add(new_note)
    database.commit()
    database.refresh(new_note)
    return new_note


def get_user_notes(user_id: int) -> list[Note]:
    database = get_database_session()

    try:
        notes = database.query(Note).filter(Note.owner_id == user_id).all()
        return notes

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Could not retrieve notes: {}".format(str(e)),
        )
        
    finally:
        database.close()
