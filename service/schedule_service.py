import logging
from datetime import datetime

import schedule
import time

from common import log
from common.slack_utils import SlackUtils
from entity.backup_info import BackupInfo
from enum_class.status import Status
from service import backup_info_service
from service import backup_service
from service.backup_info_service import DatabaseInfoService


class ScheduleService:
    running: bool = False
    database_info_service = None

    def __init__(self, database_info_service: DatabaseInfoService) -> None:
        self.database_info_service = database_info_service
        super().__init__()

    def job(self):
        if self.running:
            print("SKIP")
        else:
            try:
                self.running = True
                log.info("I'm working...")
                conditions = BackupInfo()
                conditions.delete_flg = 0
                lst = self.database_info_service.find_list_database_info(conditions)
                if lst:
                    for info in lst:
                        now = datetime.now()
                        if '[]'.__eq__(info.dump_time) and (
                                not info.last_run
                                or not info.last_run.strftime("%Y/%m/%d").__eq__(now.strftime("%Y/%m/%d"))):
                            result = backup_service.process(info)
                            if result.status == Status.OK:
                                info.last_run = datetime.now()
                                self.database_info_service.insert_or_update(info)
                                color = '#1666EE'
                            else:
                                color = '#FF4040'
                            SlackUtils.post_message(db_info=info, result=result.data, color=color)
                self.running = False
            except Exception as e:
                self.running = False
                log.error(e)

    # schedule.every(1).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
    # schedule.every().minute.at(":17").do(job)

    def init_schedule(self):
        while True:
            self.job()
            time.sleep(10)
