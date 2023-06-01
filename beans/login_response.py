from typing import Any

from pydantic import BaseModel, EmailStr


class LoginResponse(BaseModel):
    email: EmailStr = None
    username: str = None
    token: str = None

    # def __new__(cls) -> Any:
    #     return super().__new__(cls)

    def __new__(cls, email: EmailStr = None, username: str = None, token: str = None) -> Any:
        cls.email = email
        cls.username = username
        cls.token = token
        return super().__new__(cls)
