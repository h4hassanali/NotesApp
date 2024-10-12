from fastapi import FastAPI
from .initialize_tables import initialize_tables
from user.routes import user_router
from note.routes import note_router

app = FastAPI()

initialize_tables()

app.include_router(user_router, prefix="/user")
app.include_router(note_router, prefix="/note")
