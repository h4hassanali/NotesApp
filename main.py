from fastapi import FastAPI
from database import migrations
from user.routes import user_router
from note.routes import note_router

app = FastAPI()

migrations.migrate()

app.include_router(user_router, prefix = "/user")
app.include_router(note_router, prefix = "/note")
