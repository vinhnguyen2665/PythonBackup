import copy
import os
import re

from beans.result_object import ResultObject
from common import file_utils, database_utils, log
from common.svn_utils import SvnUtils
from enum_class.backup_type import BackupType
from enum_class.status import Status
import service.mongo_db_service as mongo_db_service
import service.mysql_service as mysql_service
from entity.backup_info import BackupInfo
from common.shell_exec import read_completed_process
from enum_class.svn_status import SvnStatus
from service import scp_service


def gen_key_name(key: str, _map: any, index: int = 0):
    if _map.__contains__(key):
        index += 1
        return gen_key_name(key + '_' + str(index), _map, index)
    else:
        return key


def process(db_info: BackupInfo):
    try:
        access = file_utils.access_permission(db_info.dump_dir, os.W_OK)
        if not access and not file_utils.is_exist(db_info.dump_dir):
            out = SvnUtils.check_out(db_info)
            log.info(out.data)  # checkout svn
            access = file_utils.access_permission(db_info.dump_dir, os.W_OK)

        if access:
            switcher = {
                BackupType.MySQL: lambda: database_backup(db_info),
                BackupType.MongoDB: lambda: database_backup(db_info),
                BackupType.SCP: lambda: scp_service.pull(db_info),
            }
            p = switcher.get(db_info.backup_type, lambda: ResultObject(status=Status.ERROR,message='Invalid Backup Type', data='Invalid Backup Type'))
            return p()
        else:
            return ResultObject(Status.ERROR, 'Permission Denied ', db_info.dump_dir)
    except Exception as e:
        log.error(e)
        return ResultObject(Status.ERROR, e.__class__, e)


def database_backup(db_info: BackupInfo):
    step_arr = []
    if not file_utils.is_exist(db_info.dump_dir):
        out = SvnUtils.check_out(db_info)
        step_arr += out.data
    version = get_version(db_info)  # get version
    if version.status == Status.OK:
        step_arr.append("Version: " + version.data)
        db_info.version_name = version.data
    else:
        return version
    d = dump(db_info)
    dump_tmp = copy.deepcopy(d)  # dump database

    dump_result_map = {}
    error = False
    error_arr = []
    for svn_info in dump_tmp.data:
        t_var = svn_info.split(':')[0]
        v_var = svn_info[len(t_var) + 1:].strip()
        # if dump_result_map.__contains__('dump_path'):
        if v_var.startswith('Error'):
            error = True
            error_arr.append(v_var)
        dump_result_map[gen_key_name(key=t_var, _map=dump_result_map)] = v_var
    step_arr = step_arr + dump_tmp.data
    # svn
    commit_dir = SvnUtils.commit_dir(db_info)
    step_arr += commit_dir.data

    # if dump_result_map.__contains__('dump_path'):
    #     print("")
    # el
    if error:
        return ResultObject(Status.ERROR, 'Error', error_arr)
    else:
        if dump_result_map.__contains__('dump_path'):
            info = SvnUtils.info(db_info, dump_result_map.get('dump_path'))
            if info and info.url:
                step_arr.append("svn_url:" + info.url)
        return ResultObject(Status.OK, step_arr, step_arr)


def get_version(db_info: BackupInfo):
    switcher = {
        BackupType.MySQL: lambda: mysql_service.get_version(db_info),
        BackupType.MongoDB: lambda: mongo_db_service.get_version(db_info),
    }
    ver = switcher.get(db_info.backup_type, lambda: ResultObject(status=Status.ERROR, data='Invalid Database'))
    return read_completed_version(ver())


def dump(db_info: BackupInfo):
    switcher = {
        BackupType.MySQL: lambda: mysql_service.dump(db_info),
        BackupType.MongoDB: lambda: mongo_db_service.dump(db_info),
    }
    d = switcher.get(db_info.backup_type, lambda: ResultObject(status=Status.ERROR, data='Invalid Database'))
    return read_completed_process(d())


def read_completed_version(shell_out):
    version = ''
    msg = []
    if shell_out:
        for out in shell_out:
            tmp = out.decode("utf-8")
            re_flg = re.search("^[0-9]+(\\.[0-9]+)*", tmp)
            msg.append(tmp)
            if re_flg:
                version = tmp.replace('\r\n', '').replace('\n', '')
    if version:
        return ResultObject(status=Status.OK, message=msg, data=version)
    else:
        return ResultObject(status=Status.ERROR, message=msg, data=msg)
