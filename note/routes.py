from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.dependencies import get_database_session
from services.note_services import (
    service_to_create_note,
    service_to_get_user_notes,
)
from .schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse
from .models import Note
from user.utils import check_user

note_router = APIRouter()


# Add Note Route
@note_router.post(
    "/add_note",
    response_model=AddNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_note(
    note_data: AddNoteRequest,
    database: Session = Depends(get_database_session),
):
    # Check if user exists
    check_user(user_id=note_data.user_id, database=database)

    new_note = service_to_create_note(note_data, database)

    return new_note


# View Notes Route
@note_router.get(
    "/view_notes",
    response_model=ListNotesResponse,
    status_code=status.HTTP_200_OK,
)
def view_notes(
    user_id: int, database: Session = Depends(get_database_session)
):
    # Check if user exists
    check_user(user_id=user_id, database=database)

    notes = service_to_get_user_notes(user_id, database)

    # Return the notes in a structured response
    return {"notes": notes}
