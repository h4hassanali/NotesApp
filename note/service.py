from sqlalchemy.orm import Session
from note.models import Note
from note.schemas import AddNoteRequest
from database.service import get_database_session


def create_note_service(note_data: AddNoteRequest, user_id: int):
    with get_database_session() as database:
        return create_note_in_db(database, note_data, user_id)


def create_note_in_db(database: Session, note_data: AddNoteRequest, user_id: int):
    new_note = Note(
        title = note_data.title,
        content = note_data.content,
        owner_id = user_id,
    )
    database.add(new_note)
    database.commit()
    database.refresh(new_note)
    return new_note


def get_notes_service(user_id: int) -> list[Note]:
    with get_database_session() as database:
        notes = database.query(Note).filter(Note.owner_id == user_id).all()
        return notes
