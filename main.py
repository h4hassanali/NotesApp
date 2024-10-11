from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models
from database.db import SessionLocal, engine 

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(name: str, email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/signin")
def siginin(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return f"Welcome {user.name}, you have Loged into the System"
    raise HTTPException(status_code=400, detail="User not found")

@app.post("/add_note")
def add_note(user_id: int, title: str, content: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    new_note = models.Note(title=title, content=content, owner_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/read_note")
def read_notes(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    notes = db.query(models.Note).filter(models.Note.owner_id == user_id).all()
    return notes
