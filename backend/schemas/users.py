from models.users import User
from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateUserPayload(BaseModel):
    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(..., description="The password of the user", min_length=8)
    confirm_password: str = Field(
        ..., description="The confirm password of the user", min_length=8
    )

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and confirm password do not match")
        return self


class CreateUserResponse(BaseModel):
    user: User = Field(..., description="The user created")
    message: str = Field(..., description="The message of the response")


class UpdateUserPayload(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
