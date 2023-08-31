from typing import Any

from pydantic import BaseModel, EmailStr

from enum_class.status import Status


class MyResponse(BaseModel):
    status: Status = None
    message: Any = None
    data: Any = None

    # def __new__(cls) -> Any:
    #     return super().__new__(cls)

    def __new__(cls, status: Status = None, message: Any = None, data: Any = None) -> Any:
        cls.status = status
        cls.message = message
        cls.data = data
        # return super().__new__(cls)
        return super().__new__(cls)

