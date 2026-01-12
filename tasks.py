from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks")
def create_task(title: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = models.Task(title=title, user_id=user.id)
    db.add(task)
    db.commit()
    return {"message": "Task created"}

@router.get("/tasks")
def get_tasks(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.user_id == user.id).all()
