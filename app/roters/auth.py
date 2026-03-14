from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate
from ..security import hash_password, verify_password, create_access_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user_data.password)

    db_user = User(
        email=user_data.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):

    stmt = select(User).filter_by(email=user_data.email)
    db_user = db.execute(stmt).scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }