from enum_class.backup_type import BackupType
from typing import Any

from enum_class.status import Status


class ResultObject:
    status: Status
    message: any
    data: any

    def __new__(cls, status: Status = Status.OK, message: any = None, data: Any = None) -> Any:
        cls.status = status
        cls.message = message
        cls.data = data
        # return super().__new__(cls)
        return cls

    # def __new__(cls, status: Status, message: str = '') -> Any:
    #     cls.status = status
    #     cls.message = message
    #     return super().__new__(cls)
    #
    # def __new__(cls, status: Status, data: Any) -> Any:
    #     cls.status = status
    #     cls.data = data
    #     return super().__new__(cls)

    # def __new__(cls, status: Status = Status.OK, message: any = None, data: Any = None) -> Any:
    #     cls.status = status
    #     cls.message = message
    #     cls.data = data
    #     return super().__new__(cls)
    #     # return super().__new__(cls)
    def __init__(self, status: Status = Status.OK, message: any = None, data: Any = None) -> None:
        self.status = status
        self.message = message
        self.data = data
        # super().__init__()

    def __repr__(self):
        repr_format = "status: {status}, " \
                      "message: {message}, " \
                      "data: {data}"
        return repr_format.format(status=self.status, message=self.message, data=self.data)
