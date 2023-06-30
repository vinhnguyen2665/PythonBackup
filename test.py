import os
from datetime import datetime

import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler

from common import file_utils, database_utils, resource_utils
from common.slack_utils import SlackUtils
from common.sys_utils import shell_detector
from entity.backup_info import BackupInfo
from enum_class.authentication_method import AuthenticationMethod
from enum_class.backup_type import BackupType
from common.svn_utils import SvnUtils
import json

from enum_class.svn_status import SvnStatus
from common.shell_exec import read_completed_process
from orm_config.init_orm import OrmConfig
from service import backup_service, scp_service
from service.backup_info_service import DatabaseInfoService


def test1():
    db_info = BackupInfo()
    db_info.__init__(host='35.187.197.125',
                     port=3306,
                     username='root',
                     password='Srv@20210330',
                     backup_type=BackupType.MySQL,
                     database_name='rfid',
                     skip_lock_table=True,
                     column_statistics=0,
                     dump_dir='/var/www/backup_db/rfid',
                     mentions=json.dumps(['<@UEJSM23ML>']),
                     svn_url='https://nsmp-system.com/svn/backup_db/rfid/',
                     svn_username='vinhnq',
                     svn_password='vinh1996')

    # mentions = ['<@U012Q4ED5NJ>', '<!channel>']

    # result = SvnUtils.check_out(db_info)

    result = backup_service.dump(db_info)
    # result = backup_service.process(db_info)
    # result = ['Tesst', 'Tesst', 'Tesst', 'Tesst', 'Tesst', 'svn_url: https://google.com']
    print(result)
    # SlackUtils.post_message(db_info, result.data)
    # tmp = read_completed_process(out, err)
    # print(tmp.message)
    # out = SvnUtils.update(db_info.dump_dir)
    # tmp = read_completed_process(out)
    # print(tmp.message)
    # SlackUtils.post_message(db_info)


def test_mongo():
    db_info = BackupInfo()
    db_info.__init__(host='172.18.101.75',
                     port=27017,
                     username='root',
                     password='123456',
                     backup_type=BackupType.MongoDB,
                     database_name='kotei_shisan',
                     authentication_database='admin',
                     dump_dir='/var/www/backup_db/kotei_shisan',
                     mentions=json.dumps(['<@UEJSM23ML>']),
                     svn_url='https://nsmp-system.com/svn/backup_db/kotei_shisan/',
                     svn_username='vinhnq',
                     svn_password='vinh1996')

    # mentions = ['<@U012Q4ED5NJ>', '<!channel>']

    # result = SvnUtils.check_out(db_info)

    result = backup_service.dump(db_info)
    # result = backup_service.process(db_info)
    # result = ['Tesst', 'Tesst', 'Tesst', 'Tesst', 'Tesst', 'svn_url: https://google.com']
    print(result)
    # SlackUtils.post_message(db_info, result.data)
    # tmp = read_completed_process(out, err)
    # print(tmp.message)
    # out = SvnUtils.update(db_info.dump_dir)
    # tmp = read_completed_process(out)
    # print(tmp.message)
    # SlackUtils.post_message(db_info)


def init_db():
    # mentions = ['<@U012Q4ED5NJ>', '<!channel>']
    # db_info = BackupInfo(host='103.1.210.79',
    #                        port=3306,
    #                        username='root',
    #                        password='srv099999',
    #                        backup_type=BackupType.MySQL,
    #                        database_name='backupdatabasemanager',
    #                        skip_lock_table=True,
    #                        column_statistics=0,
    #                        dump_dir='/var/www/backup_db/backupdatabasemanager',
    #                        mentions=json.dumps(['<@UEJSM23ML>']),
    #                        svn_url='https://nsmp-system.com/svn/backup_db/test/',
    #                        svn_password='vinh1996',
    #                        svn_username='vinhnq')
    # db_info.create_date = datetime.now()
    # db_info.create_id = 0
    # database_info_service.insert_or_update(db_info)
    db_connect = OrmConfig()
    database_info_service = DatabaseInfoService(db_connect)
    db_info = BackupInfo(host='103.1.210.79',
                         port=3306,
                         username='root',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='backupdatabasemanager',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/backupdatabasemanager',
                         mentions=json.dumps(['<@UEJSM23ML>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/backupdatabasemanager/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='34.84.179.153',
                         port=33306,
                         username='nd_user',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='ndcore_release',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/ndcore_release',
                         mentions=json.dumps(['<@UEJSM23ML>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/ndcore_release/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='34.85.41.87',
                         port=3306,
                         username='nsmv_backup',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='morisada_release',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/morisada_release',
                         mentions=json.dumps(['<@U3DA4PCCW>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/morisada_release/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='34.85.41.87',
                         port=3306,
                         username='nsmv_backup',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='hiroshima',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/hiroshima',
                         mentions=json.dumps(['<@U3DA4PCCW>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/hiroshima/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='34.85.41.87',
                         port=3306,
                         username='nsmv_backup',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='nagoya',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/nagoya',
                         mentions=json.dumps(['<@U3DA4PCCW>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/nagoya/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='35.187.197.125',
                         port=3306,
                         username='nsmv_backup',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='niji_yusho',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/niji_yusho',
                         mentions=json.dumps(['<@U3DA4PCCW>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/niji_yusho/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='34.146.93.98',
                         port=3306,
                         username='buzen',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='buzen',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/buzen',
                         mentions=json.dumps(['<@UKSL05XNK>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/buzen/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='35.187.197.125',
                         port=3306,
                         username='root',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='rfid_sendai',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/rfid_sendai',
                         mentions=json.dumps(['<@UEJSM23ML>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/rfid_sendai/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)

    db_info = BackupInfo(host='34.85.41.87',
                         port=3306,
                         username='nsmv_backup',
                         password='Zk@jB27n*gE7hd)(^%',
                         backup_type=BackupType.MySQL,
                         database_name='millsheet',
                         skip_lock_table=True,
                         column_statistics=0,
                         dump_dir='/var/www/backup_db/millsheet',
                         mentions=json.dumps(['<@UAGV4LJ6R>']),
                         svn_url='https://nsmp-system.com/svn/backup_db/millsheet/',
                         svn_password='vinh1996',
                         svn_username='vinhnq')
    db_info.create_date = datetime.now()
    db_info.create_id = 0
    database_info_service.insert_or_update(db_info)


def test_db_2():
    db_connect = OrmConfig()
    database_info_service = DatabaseInfoService(db_connect)

    conditions = BackupInfo()
    conditions.delete_flg = 2
    lst = database_info_service.find_list_database_info(conditions)
    for db_info in lst:
        # result = backup_service.dump(db_info)
        result = backup_service.process(db_info)
        # result = ['Tesst', 'Tesst', 'Tesst', 'Tesst', 'Tesst', 'svn_url: https://google.com']
        print(str(result.status) + ' ' + str(result.data))


def test_scp():
    db_connect = OrmConfig()
    db_info = BackupInfo()
    db_info.__init__(host='172.18.101.75',
                     port=22,
                     username='nsmv',
                     password='123456',
                     backup_type=BackupType.SCP,
                     remote_folder='/var/www/shashin_kyoyu',
                     authentication_method=AuthenticationMethod.Password,
                     dump_dir='/var/www/backup_db/shashin_kyoyu_resources',
                     mentions=json.dumps(['<@UEJSM23ML>']),
                     svn_url='https://nsmp-system.com/svn/backup_db/kotei_shisan/',
                     svn_username='vinhnq',
                     svn_password='vinh1996')
    # db_info.__init__(host='35.243.88.196',
    #                  port=22,
    #                  username='vinhnq',
    #                  backup_type=BackupType.SCP,
    #                  remote_folder='/var/www/Morisada',
    #                  authentication_method=AuthenticationMethod.PublicKey,
    #                  dump_dir='/var/www/backup_db/morisada_resource',
    #                  mentions=json.dumps(['<@UEJSM23ML>']),
    #                  svn_url='https://nsmp-system.com/svn/backup_db/kotei_shisan/',
    #                  svn_username='vinhnq',
    #                  svn_password='vinh1996')

    r = backup_service.process(db_info)
    # r = scp_service.local_walk(db_info.dump_dir)
    print(r)
    # local = scp_service.convert_remote2local_dir(root_remote_path='/var/www/shashin_kyoyu/',
    #                                      root_local_path='/var/www/backup_db/shashin_kyoyu_resource',
    #                                      remote_path='/var/www/shashin_kyoyu/tmp/20230223_165908_261.jpeg')
    # print(local)


def test_mongo():
    # db_info = BackupInfo()
    # db_info.__init__(host='103.1.210.79',
    #                      port=3306,
    #                      username='root',
    #                      password='Zk@jB27n*gE7hd)(^%',
    #                      backup_type=BackupType.MySQL,
    #                      database_name='backupdatabasemanager',
    #                      skip_lock_table=True,
    #                      column_statistics=0,
    #                      dump_dir='/var/www/backup_db/backupdatabasemanager',
    #                      mentions=json.dumps(['<@UEJSM23ML>']),
    #                      svn_url='https://nsmp-system.com/svn/backup_db/backupdatabasemanager/',
    #                      svn_password='vinh1996',
    #                      svn_username='vinhnq')
    # path_exec = database_utils.choose_exec_query_path(db_info)
    # resource_utils.download_third_party_resource(path_exec)
    #
    # path_exec = os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x64", "mysqld")
    # resource_utils.download_third_party_resource(path_exec)

    db_info = BackupInfo()
    db_info.__init__(host='34.146.65.207',
                     port=27017,
                     username='root',
                     password='Nsmv20231553~',
                     backup_type=BackupType.MongoDB,
                     database_name='shashin_kyoyu',
                     authentication_database='admin',
                     dump_dir='/var/www/backup_db/shashin_kyoyu',
                     mentions=json.dumps(['<@UEJSM23ML>']),
                     svn_url='https://nsmp-system.com/svn/backup_db/shashin_kyoyu/',
                     svn_username='vinhnq',
                     svn_password='vinh1996')

    get_version = backup_service.dump(db_info)
    print(get_version.data)


def test_zip():
    file_utils.zip_file('/var/www/backup_db/nogigps/2023.05.09/nogigps_2023.05.09_10.25.36.688.sql',
                        '/var/www/backup_db/nogigps/2023.05.09/nogigps_2023.05.09_10.25.36.688.zip')


def test_apscheduler():
    scheduler = BackgroundScheduler()

    def some_job():
        time.sleep(15)
        print(f"{datetime.datetime.utcnow()}: Every 10 seconds")

    job = scheduler.add_job(some_job, 'interval', seconds=10, max_instances=1)

    scheduler.start()
    try:
        while True:
            time.sleep(1)
    finally:
        scheduler.shutdown()


if __name__ == '__main__':
    test_scp()
