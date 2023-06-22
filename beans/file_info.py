from datetime import datetime

from enum_class.file_type import FileType


class FileInfo:
    file_type: FileType
    path: str
    access_time: datetime
    last_modified: datetime
    permissions: str

    def __init__(self,
                 file_type: FileType = FileType.UNKNOWN,
                 path: str = None,
                 access_time: datetime = None,
                 last_modified: datetime = None,
                 permissions: str = None):
        self.file_type = file_type
        self.path = path
        self.access_time = access_time
        self.last_modified = last_modified
        self.permissions = permissions
        super().__init__()

    def __new__(cls,
                file_type: FileType = FileType.UNKNOWN,
                path: str = None,
                access_time: datetime = None,
                last_modified: datetime = None,
                permissions: str = None):
        cls.file_type = file_type
        cls.path = path
        cls.access_time = access_time
        cls.last_modified = last_modified
        cls.permissions = permissions
        return super().__new__(cls)

    # def __new__(cls):
    #     return super().__new__(cls)
