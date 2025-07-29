from fastapi import APIRouter
from app.services import user as user_service

router = APIRouter()

@router.post("/users/")
async def create_user(user: user_service.UserCreate):
    return await user_service.create_user(user)

@router.get("/users/")
async def read_users():
    return await user_service.get_users()

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return await user_service.delete_user(user_id)