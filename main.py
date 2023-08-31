import threading

from controller.endpoints import authorization, backup_api
from orm_config.init_orm import OrmConfig
from service.schedule_service import ScheduleService
import logging

import uvicorn
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from service.backup_info_service import DatabaseInfoService


def init_schedule(database_info_service: DatabaseInfoService):
    schedule_service = ScheduleService(database_info_service)
    schedule_service.init_schedule()


def init_uvicorn():
    uvicorn.run(app, host='0.0.0.0', port=8000)


app = FastAPI(
    title='FastAPI JWT',
    openapi_url='/openapi.json',
    # docs_url=None,  # Disable docs (Swagger UI)
    # redoc_url=None,  # Disable redoc
    docs_url='/',
    description='fastapi jwt'
)

app.include_router(authorization.authorization_router, prefix="/api/auth", tags=["authorization"])
app.include_router(backup_api.backup_api_router, prefix="/api/backup", tags=["backup_api"])


@app.get(path='/docs')
def alive():
    return "Alive"


db_connect = None
if __name__ == '__main__':
    load_dotenv()
    log_format = '%(asctime)s %(process)d-%(levelname)s-%(message)s'
    logging.basicConfig(filename='database_backup.log',
                        level=logging.DEBUG,
                        format=log_format)

    db_connect = OrmConfig()
    database_info_service = DatabaseInfoService(db_connect)

    thread = threading.Thread(target=init_uvicorn)
    thread.start()

    thread2 = threading.Thread(target=init_schedule(database_info_service))
    thread2.start()
    # test()
