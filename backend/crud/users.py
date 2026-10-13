from models.users import User
from pydantic import EmailStr
from schemas.users import CreateUserPayload, UpdateUserPayload
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.security import generate_hash


class UserService:
    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_by_email(
        self,
        user_email: EmailStr,
        session: AsyncSession,
    ):
        statement = select(User).where(User.email == user_email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(
        self,
        email: EmailStr,
        session: AsyncSession,
    ) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(
        self,
        user_data: CreateUserPayload,
        session: AsyncSession,
    ):
        # Check whether the email is already registered.
        if await self.user_exists(user_data.email, session):
            return None

        # Create the database model from the validated payload.
        user_data_dict = user_data.model_dump(
            exclude={"confirm_password"},
        )

        new_user = User(**user_data_dict)
        new_user.password_hash = await generate_hash(user_data_dict["password"])

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    async def update_user(
        self,
        email: EmailStr,
        update_data: UpdateUserPayload,
        session: AsyncSession,
    ):
        user_to_update = await self.get_user_by_email(email, session)

        if user_to_update is None:
            return None

        update_user_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_user_dict.items():
            setattr(user_to_update, key, value)

        await session.commit()
        await session.refresh(user_to_update)

        return user_to_update

    async def delete_user(
        self,
        email: EmailStr,
        session: AsyncSession,
    ) -> bool:
        user_to_delete = await self.get_user_by_email(email, session)

        if user_to_delete is None:
            return False

        await session.delete(user_to_delete)
        await session.commit()

        return True


user_service = UserService()
