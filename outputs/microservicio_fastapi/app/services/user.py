from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.db import get_db

async def create_user(user: UserCreate):
    db = Session(bind=get_db())
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_users():
    db = Session(bind=get_db())
    return db.query(User).all()

async def delete_user(user_id: int):
    db = Session(bind=get_db())
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}