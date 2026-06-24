from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.security import hash_password
from app.database.dependencies import get_db
from app.database.models import User
from app.schemas.user import SignupRequest

router = APIRouter()

@router.post("/signup")
def create_user(
    user: SignupRequest,
    db: Session = Depends(get_db)
):

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()

