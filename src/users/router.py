from fastapi import APIRouter, Depends
from fastapi import status

from src.auth.service import CurrentUser
from src.users import service, validators
from src.users.schemas import UserRead, UserCreate
from src.database import AsyncDbSession

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(
        session: AsyncDbSession,
        user_in: UserCreate = Depends(validators.valid_user_create),
):
    user = await service.create_user(session, user_in)
    await session.commit()
    return user


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user
