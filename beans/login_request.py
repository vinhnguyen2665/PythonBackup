from typing import Any

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

    def __new__(cls, username: str = None, password: str = None):
        cls.username = username
        cls.password = password
        return super().__new__(cls)

