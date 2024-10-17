from sqlalchemy.orm import Session
from note.models import Note
from note.schemas import AddNoteRequest
from database.service import get_database_session


def create_note_service(note_data: AddNoteRequest):
    database = get_database_session()
    try:
        return create_note_in_db(database, note_data)
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


def get_notes_service(user_id: int) -> list[Note]:
    database = get_database_session()
    try:
        notes = database.query(Note).filter(Note.owner_id == user_id).all()
        return notes
    finally:
        database.close()
