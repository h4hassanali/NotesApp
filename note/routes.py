from fastapi import Depends, APIRouter, status, HTTPException, Security, BackgroundTasks
from user.models import User
from user.dependencies import get_current_user
from note.service import create_note_service, get_notes_service
from user.logging import log_user_action
from .schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse

note_router = APIRouter()


@note_router.post("/notes", response_model = AddNoteResponse, status_code = status.HTTP_201_CREATED)
def create_note(note_data: AddNoteRequest, background_task: BackgroundTasks, current_user: User = Security(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token. Please log in again.",
        )
    new_note = create_note_service(note_data, current_user.id)
    background_task.add_task(log_user_action, current_user.id, "Added a Note")
    return new_note


@note_router.get("/notes", response_model = ListNotesResponse, status_code = status.HTTP_200_OK)
def get_notes(background_task: BackgroundTasks, current_user: User = Security(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token. Please log in again.",
        )
    notes = get_notes_service(current_user.id)
    background_task.add_task(log_user_action, current_user.id, "Get Notes")
    return {"notes": notes}
