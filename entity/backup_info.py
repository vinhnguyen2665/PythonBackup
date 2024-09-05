from sqlalchemy import String, Integer, Boolean, Column, Enum, Date
from sqlalchemy.ext.declarative import declarative_base

from enum_class.authentication_method import AuthenticationMethod
from enum_class.backup_type import BackupType

Base = declarative_base()


class BackupInfo(Base):
    __tablename__ = "backup_info"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    port = Column(Integer)
    database_name = Column(String)
    authentication_database = Column(String)
    username = Column(String)
    password = Column(String)
    version_code = Column(Integer)
    version_name = Column(String)
    backup_type = Column(Enum(BackupType))
    skip_lock_table = Column(Boolean)
    column_statistics = Column(Integer)
    no_table_spaces = Column(Boolean)
    routines = Column(String)
    create_schema = Column(String)
    remote_folder = Column(String)
    authentication_method = Column(Enum(AuthenticationMethod))
    dump_time = Column(String)
    dump_dir = Column(String)
    mentions = Column(String)
    svn_url = Column(String)
    svn_username = Column(String)
    svn_password = Column(String)
    last_run = Column(Date)
    create_date = Column(Date)
    create_id = Column(Integer)
    update_date = Column(Date)
    update_id = Column(Integer)

    delete_flg = Column(Integer)

    def __new__(cls):
        return super().__new__(cls)
    # def __new__(cls,
    #             host: str,
    #             port: int,
    #             database_name: Column(Integer),
    #             authentication_database: str = None,
    #             username: str = None,
    #             password: str = None,
    #             backup_type: BackupType = None,
    #             dump_dir: str = None,
    #             skip_lock_table: bool = False,
    #             column_statistics: int = None,
    #             mentions: str = '[]',
    #             dump_time: str = '[]',
    #             svn_url: str = None,
    #             svn_username: str = None,
    #             svn_password: str = None,
    #             delete_flg: int = None, ) -> None:
    #     cls.host = host
    #     cls.port = port
    #     cls.database_name = database_name
    #     cls.authentication_database = authentication_database
    #     cls.username = username
    #     cls.password = password
    #     cls.backup_type = backup_type
    #     cls.dump_dir = dump_dir
    #     cls.skip_lock_table = skip_lock_table
    #     cls.column_statistics = column_statistics
    #     cls.dump_time = dump_time
    #     cls.mentions = mentions
    #     cls.svn_url = svn_url
    #     cls.svn_username = svn_username
    #     cls.svn_password = svn_password
    #     cls.delete_flg = delete_flg
    #     return super().__new__(cls)

    def __init__(self,
                 host: str = None,
                 port: int = None,
                 database_name: str = None,
                 authentication_database: str = None,
                 username: str = None,
                 password: str = None,
                 backup_type: BackupType = None,
                 dump_dir: str = None,
                 skip_lock_table: bool = False,
                 column_statistics: int = None,
                 routines: str = '0',
                 create_schema: str = '0',
                 mentions: str = '[]',
                 dump_time: str = '[]',
                 svn_url: str = None,
                 svn_username: str = None,
                 svn_password: str = None,
                 delete_flg: int = None,
                 authentication_method: AuthenticationMethod = None,
                 remote_folder: str = None) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        self.authentication_database = authentication_database
        self.username = username
        self.password = password
        self.backup_type = backup_type
        self.dump_dir = dump_dir
        self.skip_lock_table = skip_lock_table
        self.column_statistics = column_statistics
        self.routines = routines
        self.create_schema = create_schema
        self.dump_time = dump_time
        self.mentions = mentions
        self.svn_url = svn_url
        self.svn_username = svn_username
        self.svn_password = svn_password
        self.delete_flg = delete_flg
        self.authentication_method = authentication_method
        self.remote_folder = remote_folder

    def __str__(self):
        return self.backup_type.__str__() + ": " + self.host + ":" + str(self.port)
