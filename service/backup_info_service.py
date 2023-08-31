from sqlalchemy import and_

from common import log
from entity.backup_info import BackupInfo
from orm_config.init_orm import OrmConfig


class DatabaseInfoService:
    dbConnect = None

    def __init__(self, db_connect: OrmConfig) -> None:
        self.dbConnect = db_connect
        super().__init__()

    def find_list_database_info(self, conditions: BackupInfo):
        try:
            session = self.dbConnect.get_session()
            # query = session.query(BackupInfo).where(
            #     BackupInfo.delete_flg == conditions.delete_flg
            # )

            # conditions.database_name
            # OR
            # BackupInfo.database_name == conditions.database_name,
            query = session.query(BackupInfo) \
                .filter(and_(BackupInfo.database_name == conditions.database_name if conditions.database_name is not None else True,
                             BackupInfo.delete_flg == conditions.delete_flg if conditions.delete_flg is not None else True
                             ))
            result = query.all()
            # print(query)
            return result
        except Exception as e:
            log.error(e)

    def insert(self, database_info: BackupInfo):
        try:
            session = self.dbConnect.get_session()
            session.add(database_info)
            session.commit()
        except Exception as e:
            log.error(e)

    def insert_or_update(self, database_info: BackupInfo):
        try:
            session = self.dbConnect.get_session()
            session.merge(database_info)
            session.commit()
            session.flush()
        except Exception as e:
            log.error(e)
