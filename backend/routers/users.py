from crud.users import user_service
from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from schemas.users import (
    CreateUserPayload,
    CreateUserResponse,
    UpdateUserPayload,
)
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter()


@auth_router.get("/auth", tags=["users"])
async def get_all_users(session: AsyncSession):
    users = await user_service.get_all_users(session)
    return users


@auth_router.get("/auth/{email}", tags=["users"])
async def get_user_by_email(
    email: EmailStr,
    session: AsyncSession,
):
    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@auth_router.post(
    "/auth",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
async def create_user(
    user_payload: CreateUserPayload,
    session: AsyncSession,
) -> CreateUserResponse:
    user = await user_service.create_user(user_payload, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    return CreateUserResponse(
        user=user,
        message="User created successfully",
    )


@auth_router.patch(
    "/auth/{email}",
    tags=["users"],
)
async def update_user(
    email: EmailStr,
    update_payload: UpdateUserPayload,
    session: AsyncSession,
):
    user = await user_service.update_user(
        email,
        update_payload,
        session,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@auth_router.delete(
    "/auth/{email}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
)
async def delete_user(
    email: EmailStr,
    session: AsyncSession,
) -> None:
    deleted = await user_service.delete_user(email, session)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
