from fastapi import APIRouter, Depends, status, HTTPException, Security, BackgroundTasks
from auth.service import admin_required, user_required
from user.models import User
from user.common_services import get_current_user
from note.service import create_note_service, get_notes_service
from utils.logging import log_user_action
from note.schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse

note_router = APIRouter()


@note_router.post("/notes", response_model = AddNoteResponse, status_code = status.HTTP_201_CREATED)
def create_note(note_data: AddNoteRequest, background_task: BackgroundTasks, current_user: User = Depends(user_required)):
    if current_user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token. Please log in again.",
        )
    if current_user == False:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not Enough Permissions" 
        )
    new_note = create_note_service(note_data, current_user.id)
    background_task.add_task(log_user_action, current_user.id, "Added a Note")
    return new_note


@note_router.get("/notes", response_model = ListNotesResponse, status_code = status.HTTP_200_OK)
def get_notes(background_task: BackgroundTasks, current_user: User = Depends(user_required)):
    if current_user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token. Please log in again.",
        )
    if current_user == False:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not Enough Permissions"
        )
    notes = get_notes_service(current_user.id)
    background_task.add_task(log_user_action, current_user.id, "Get Notes")
    return {"notes": notes}

