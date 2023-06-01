from enum_class.backup_type import BackupType
from typing import Any

from enum_class.status import Status
from enum_class.svn_status import SvnStatus


class SvnStatusObject:
    status: SvnStatus
    path: str

    # def __new__(cls, status: SvnStatus = None, path: str = None) -> Any:
    #     cls.status = status
    #     cls.path = path
    #
    #     return super().__new__(cls)
    #     # return super().__new__(cls)

    def __init__(self, status: SvnStatus = None, path: str = None) -> Any:
        self.status = status
        self.path = path

    def __repr__(self):
        repr_format = "status: {status}, " \
                      "path: {path}, "
        return repr_format.format(status=self.status, path=self.path)
