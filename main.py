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

