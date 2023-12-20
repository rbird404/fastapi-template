from fastapi import APIRouter
from fastapi import status

from src.auth.service import CurrentUser
from src.users.schemas import UserRead, UserCreate
from src.users.use_case import CreateUser

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(
        use_case: CreateUser, user_in: UserCreate,
):
    return await use_case(user_in)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user
