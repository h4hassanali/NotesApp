from pydantic import BaseModel
from typing import List


# Schema for Add Note Request
class AddNoteRequest(BaseModel):
    title: str
    content: str
    user_id: int


# Schema for Add Note Response
class AddNoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


# Schema for View Note Response (for listing multiple notes)
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


# Schema for listing multiple notes
class ListNotesResponse(BaseModel):
    notes: List[NoteResponse]
