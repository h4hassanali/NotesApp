from fastapi import APIRouter, HTTPException, status
from note.service import (
    create_note_service,
    get_notes_service,
)
from .schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse
from user.service import check_user

note_router = APIRouter()


@note_router.post("/notes", response_model = AddNoteResponse, status_code = status.HTTP_201_CREATED)
def create_note(note_data: AddNoteRequest):
    if check_user(user_id = note_data.user_id):
        new_note = create_note_service(note_data)
        return new_note
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


@note_router.get("/notes", response_model = ListNotesResponse, status_code = status.HTTP_200_OK)
def get_notes(user_id: int):
    if check_user(user_id = user_id):
        notes = get_notes_service(user_id)
        return {"notes": notes}
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "User not found",
    )
    
