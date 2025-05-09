from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserCreate(BaseModel):
    name: str = Field(..., example="Иван Иванов")
    email: EmailStr = Field(..., example="ivan@example.com")
    password: str = Field(..., min_length=6, example="strongpassword1")

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Пароль должен быть не короче 6 символов.")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну букву.")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        return value
