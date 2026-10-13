import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: uuid.UUID = Field(..., description="The id of the user")
    email: EmailStr = Field(..., description="The email of the user")
    password_hash: str = Field(
        exclude=True, default=None, description="The password hash of the user"
    )
    created_at: datetime = Field(..., description="The created at of the user")
    updated_at: datetime = Field(..., description="The updated at of the user")
