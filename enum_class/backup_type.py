from enum import Enum


class BackupType(Enum):
    MySQL = 0
    MongoDB = 1
    PostgreSQL = 2
    SCP = 3
