from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db_session import get_db
from .schemas import AddNoteRequest, AddNoteResponse, ListNotesResponse
from .models import Note
from user.models import User
note_router = APIRouter()

# Add Note Route
@note_router.post("/add_note", response_model=AddNoteResponse, status_code=status.HTTP_201_CREATED)
def add_note(note_data: AddNoteRequest, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == note_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create a new note
    new_note = Note(title=note_data.title, content=note_data.content, owner_id=note_data.user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# View Notes Route
@note_router.get("/view_notes", response_model=ListNotesResponse, status_code=status.HTTP_200_OK)
def view_notes(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Retrieve notes for the user
    notes = db.query(Note).filter(Note.owner_id == user_id).all()

    # Return the notes in a structured response
    return {"notes": notes}