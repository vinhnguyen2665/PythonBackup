from typing import Dict, Type, Any

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends

import security.security as security
from beans.backup_info_bean import BackupInfoBean
from beans.response import MyResponse
from beans.result_object import ResultObject
from common import log
from entity.backup_info import BackupInfo
from enum_class.status import Status
from orm_config.init_orm import OrmConfig
from service import backup_service
from service.backup_info_service import DatabaseInfoService

backup_api_router = APIRouter()
db_connect = OrmConfig()
databaseInfoService = DatabaseInfoService(db_connect)


@backup_api_router.post('', dependencies=[Depends(security.validate_token)], response_model=ResultObject)
def backup(request_data: BackupInfoBean):
    try:
        condition = BackupInfo()
        condition.database_name = request_data.database_name
        condition.delete_flg = 0
        backup_list = databaseInfoService.find_list_database_info(conditions=condition)
        if list:
            for bk_info in backup_list:
                p = backup_service.process(bk_info)
                return p
        else:
            return ResultObject(status=Status.OK, message="The name database does not exist")
    except Exception as e:
        log.error(e)
        return ResultObject(status=Status.ERROR, message=e.__str__(), data=request_data)

