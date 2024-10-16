from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.dependencies import get_database_session
from note.service import (
    service_to_create_note,
    service_to_get_user_notes,
)
from .schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse
from .models import Note
from user.utils import check_user

note_router = APIRouter()


@note_router.post(
    "/add_note",
    response_model=AddNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_note(
    note_data: AddNoteRequest
):
    check_user(user_id=note_data.user_id)

    new_note = service_to_create_note(note_data)

    return new_note


@note_router.get(
    "/view_notes",
    response_model=ListNotesResponse,
    status_code=status.HTTP_200_OK,
)
def view_notes(user_id: int):
    check_user(user_id=user_id)

    notes = service_to_get_user_notes(user_id)

    return {"notes": notes}
