import os
import shutil
import sys
from datetime import datetime
from stat import S_ISDIR, S_ISREG

import filedate
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from paramiko.rsakey import RSAKey
from scp import SCPClient

from beans.file_info import FileInfo
from beans.result_object import ResultObject
from common import file_utils, log
from entity.backup_info import BackupInfo
from enum_class.authentication_method import AuthenticationMethod
from enum_class.file_type import FileType
from enum_class.status import Status


def byte_count(size, file_size):
    log.info(" transferred: {0:.0f} %".format((size / file_size) * 100))


def pull(db_info: BackupInfo):
    step_arr = []
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        if db_info.authentication_method == AuthenticationMethod.Password:
            client.connect(db_info.host, db_info.port, db_info.username, db_info.password)
        else:
            pass_phrase = os.getenv('SSH_PASSPHRASE')
            auth_file = RSAKey.from_private_key_file(os.getenv('SSH_AUTHENTICATE_FILE'), password=pass_phrase)
            client.connect(hostname=db_info.host,
                           port=db_info.port,
                           username=db_info.username,
                           pkey=auth_file,
                           passphrase=pass_phrase)
        # scp = SCPClient(client.get_transport())
    except Exception as e:
        log.error(e)
        step_arr.append(e.__str__())
        return ResultObject(Status.ERROR, db_info.__str__() + ' ' + e.__str__(), step_arr)

    sftp = client.open_sftp()
    try:
        files = walk(sftp, db_info.remote_folder)
    except Exception as e:
        log.error(e)
        step_arr.append(e.__str__())
        return ResultObject(Status.ERROR, db_info.remote_folder + ' ' + e.__str__(), step_arr)

    for file_info in files:
        local_path = convert_remote2local_dir(db_info.remote_folder, db_info.dump_dir, file_info.path)
        file_utils.if_not_exist_make_dir(file_utils.get_parent_path(local_path))
        log.info('==================' + file_info.path + '==================')
        if file_info.file_type == FileType.FILE:
            modified = is_modified(local_path, file_info)
            is_exist = file_utils.is_exist(local_path)
            if not modified:
                log.info('already exists')
            else:
                if is_exist:
                    parent_path = file_utils.get_parent_path(local_path)
                    file_name = file_utils.get_file_name_in_path(local_path)
                    if file_info.last_modified:
                        move_folder = "modified_" + file_info.last_modified.strftime("%Y_%m_%d")
                    else:
                        move_folder = "modified_" + file_utils.temp_name_from_date()
                    modified_path = os.path.join(parent_path, move_folder, file_name)
                    file_utils.if_not_exist_make_dir(file_utils.get_parent_path(modified_path))
                    shutil.move(local_path, modified_path)

                sftp.get(remotepath=file_info.path, localpath=local_path, callback=byte_count)
                # os.utime(local_path, (file_info.access_time.timestamp(), file_info.last_modified.timestamp()))
                a_file = filedate.File(local_path)
                a_file.set(
                    created=file_info.access_time.strftime("%Y-%m-%d/, %H:%M:%S"),
                    modified=file_info.last_modified.strftime("%Y-%m-%d/, %H:%M:%S"),
                    accessed=file_info.access_time.strftime("%Y-%m-%d/, %H:%M:%S")
                )
                after = filedate.File(local_path)
                print(after)

    sftp.close()
    # scp.close()


def is_modified(local_path: str, file_info: FileInfo):
    if file_utils.is_exist(local_path):
        return not datetime.fromtimestamp(os.path.getmtime(local_path)).__eq__(file_info.last_modified)
    else:
        return True


def convert_remote2local_dir(root_remote_path, root_local_path, remote_path):
    tmp = remote_path.replace(root_remote_path, '')
    if tmp.startswith(os.sep):
        tmp = tmp[len(os.sep):]
    return os.path.join(root_local_path, tmp)


def walk(sftp, remote_path):
    res = []
    for entry in sftp.listdir_attr(remote_path):
        mode = entry.st_mode
        path = remote_path + '/' + entry.filename
        m_time = datetime.fromtimestamp(entry.st_mtime)
        a_time = datetime.fromtimestamp(entry.st_atime)
        if S_ISDIR(mode):
            print(path + " is folder")
            res.append(FileInfo(file_type=FileType.DIR, path=path, access_time=a_time, last_modified=m_time))
            _walks = walk(sftp, path)
            res += _walks
        elif S_ISREG(mode):
            print(path + " is file")
            res.append(FileInfo(file_type=FileType.FILE, path=path, access_time=a_time, last_modified=m_time))
    return res
