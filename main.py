from fastapi import FastAPI, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from auth import hash_password, verify_password, create_token
from tasks import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = models.User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "User registered"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}
    return {"access_token": create_token(user.username)}

