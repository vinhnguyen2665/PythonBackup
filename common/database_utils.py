from datetime import datetime
import os
from common import file_utils
from common import sys_utils
from enum_class.backup_type import BackupType
from enum_class.platform import Platform

from entity.backup_info import BackupInfo


def generate_dump_name(db_name):
    now = datetime.now()
    current_time = db_name + "_" + now.strftime("%Y.%m.%d_%H.%M.%S.%f")[:-3]
    return current_time


def generate_dump_path(db_name, ext=''):
    now = datetime.now()
    return os.path.join(now.strftime("%Y.%m.%d"), generate_dump_name(db_name) + ext)


def choose_exec_query_path(db_info: BackupInfo):
    platform = sys_utils.platform_detector()
    path_exec = ''
    if BackupType.MySQL == db_info.backup_type:
        switcher = {
            Platform.Windows_64: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x64", "mysql.exe"),
            Platform.Windows_32: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x32", "mysql.exe"),
            Platform.Linux_32: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x32", "mysql"),
            Platform.Linux_64: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x64", "mysql"),
        }
        path_exec = switcher.get(platform, None)
    elif BackupType.MongoDB == db_info.backup_type:
        switcher = {
            Platform.Windows_64: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongosh.exe"),
            Platform.Windows_32: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongosh.exe"),
            # Platform.Linux_32: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "linux_x32", "mongosh"),
            Platform.Linux_64: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "linux_x64", "mongosh"),
        }
        path_exec = switcher.get(platform, None)

    return path_exec


def choose_exec_dump_path(db_info: BackupInfo):
    platform = sys_utils.platform_detector()
    path_exec = ''
    if BackupType.MySQL == db_info.backup_type:
        switcher = {
            Platform.Windows_64: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x64", "mysqldump.exe"),
            Platform.Windows_32: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x32", "mysqldump.exe"),
            Platform.Linux_32: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x32", "mysqldump"),
            Platform.Linux_64: os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x64", "mysqldump"),
        }
        path_exec = switcher.get(platform, None)
    elif BackupType.MongoDB == db_info.backup_type:
        switcher = {
            Platform.Windows_64: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongodump.exe"),
            Platform.Windows_32: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongodump.exe"),
            Platform.Linux_32: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "ubuntu_x86_64", "mongodump"),
            Platform.Linux_64: os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "ubuntu_x86_64", "mongodump"),
        }
        path_exec = switcher.get(platform, None)
    return path_exec
