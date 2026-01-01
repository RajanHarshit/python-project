from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal, engine
from models import Base
from schemas import SignupRequest, LoginRequest, TokenResponse
from repositories.user_repositories import UserRepository
from services.auth_service import AuthService

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(UserRepository(db))

@app.post("/signup")
def signup(
    data: SignupRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        auth_service.signup(data.email, data.password)
        return {"message": "User Created"}
    except ValueError as e:
        raise HTTPException(400, str(e))
    
@app.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = auth_service.login(data.email, data.password)
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(401, str(e))