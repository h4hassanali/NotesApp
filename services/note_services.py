# services/note_service.py
from sqlalchemy.orm import Session
from note.models import Note
from note.schemas import AddNoteRequest


def service_to_create_note(
    note_data: AddNoteRequest, database: Session
) -> Note:
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=note_data.user_id,
    )
    database.add(new_note)
    database.commit()
    database.refresh(new_note)
    return new_note


def service_to_get_user_notes(user_id: int, database: Session) -> list[Note]:
    return database.query(Note).filter(Note.owner_id == user_id).all()
