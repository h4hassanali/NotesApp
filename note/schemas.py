from pydantic import BaseModel
from typing import List


class AddNoteRequest(BaseModel):
    title: str
    content: str


class AddNoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


class ListNotesResponse(BaseModel):
    notes: List[NoteResponse]
