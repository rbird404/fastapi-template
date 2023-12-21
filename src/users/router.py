from fastapi import APIRouter, Depends
from fastapi import status

from src.users.schemas import UserCreate, UserResponse
from src.users.use_case import CreateUser, GetCurrentUser

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
        user_in: UserCreate, use_case: CreateUser = Depends(),
):
    return await use_case(user_in)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_me(use_case: GetCurrentUser = Depends()):
    return use_case()
