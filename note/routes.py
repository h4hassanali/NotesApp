from fastapi import APIRouter, status
from note.service import (
    create_note,
    get_user_notes,
)
from .schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse
from user.utils import check_user

note_router = APIRouter()


@note_router.post("/notes", response_model = AddNoteResponse, status_code = status.HTTP_201_CREATED)
def create_note(note_data: AddNoteRequest):
    check_user(user_id = note_data.user_id)
    new_note = create_note(note_data)
    return new_note


@note_router.get("/notes", response_model = ListNotesResponse, status_code = status.HTTP_200_OK)
def get_notes(user_id: int):
    check_user(user_id = user_id)
    notes = get_user_notes(user_id)
    return {"notes": notes}
