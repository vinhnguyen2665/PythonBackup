from datetime import datetime

from pydantic import BaseModel

from enum_class.authentication_method import AuthenticationMethod
from enum_class.backup_type import BackupType


class BackupInfoBean(BaseModel):
    id: int | None = None
    host: str | None = None
    port: int | None = None
    database_name: str | None = None
    authentication_database: str | None = None
    username: str | None = None
    password: str | None = None
    version_code: int | None = None
    version_name: str | None = None
    backup_type: BackupType | None = None
    skip_lock_table: bool | None = None
    column_statistics: int | None = None
    no_table_spaces: bool | None = None
    remote_folder: str | None = None
    # authentication_method: AuthenticationMethod
    dump_time: str | None = None
    dump_dir: str | None = None
    mentions: str | None = None
    svn_url: str | None = None
    svn_username: str | None = None
    svn_password: str | None = None
    last_run: datetime | None = None
    create_date: datetime | None = None
    create_id: int | None = None
    update_date: datetime | None = None
    update_id: int | None = None
    delete_flg: int | None = None

    def __new__(cls,
                id: int = None,
                host: str = None,
                port: int = None,
                database_name: str = None,
                authentication_database: str = None,
                username: str = None,
                password: str = None,
                version_code: int = None,
                version_name: str = None,
                backup_type: BackupType = None,
                skip_lock_table: bool = None,
                column_statistics: int = None,
                no_table_spaces: bool = None,
                remote_folder: str = None,
                # authentication_method: AuthenticationMethod = None,
                dump_time: str = None,
                dump_dir: str = None,
                mentions: str = None,
                svn_url: str = None,
                svn_username: str = None,
                svn_password: str = None,
                last_run: datetime = None,
                create_date: datetime = None,
                create_id: int = None,
                update_date: datetime = None,
                update_id: int = None,
                delete_flg: int = None):
        return super().__new__(cls)

    # def __new__(cls):
    #     return super().__new__(cls)

    # def __init__(self, dict1):
    #     if dict1 and dict1['authentication_method'] and type(dict1['authentication_method']) == str:
    #         dict1['authentication_method'] = AuthenticationMethod[dict1['authentication_method']]
    #     self.__dict__.update(dict1)
