import os

import common.shell_exec as shell
from entity.backup_info import BackupInfo
from common import file_utils, database_utils, log, resource_utils


def get_version(db_info: BackupInfo):
    try:
        cmd_format = "{path_exec}  " \
                     "--host={host} " \
                     "--port={port}  " \
                     "--username={user} " \
                     "--password={password} " \
                     "--authenticationDatabase={authentication_database} " \
                     "--eval \"printjson(db.version())\""
        # path_exec = os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongosh.exe")
        path_exec = database_utils.choose_exec_query_path(db_info)
        resource_utils.download_third_party_resource(path_exec)
        cmd = cmd_format.format(path_exec=path_exec,
                                host=db_info.host,
                                port=db_info.port,
                                user=db_info.username,
                                authentication_database=db_info.authentication_database,
                                password=db_info.password)
        out, err = shell.exec(cmd)
        return out
    except Exception as e:
        log.error(e)


def dump(db_info: BackupInfo):
    try:
        cmd_format = "{path_exec}  " \
                     "--host={host} " \
                     "--port={port}  " \
                     "--username={user} " \
                     "--password={password} " \
                     "--authenticationDatabase={authentication_database} " \
                     "--db={database} " \
                     "--out={dump_path}"
        path_exec = database_utils.choose_exec_dump_path(db_info)
        resource_utils.download_third_party_resource(path_exec)
        # path_exec = os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongodump.exe")
        dump_path = os.path.join(db_info.dump_dir, database_utils.generate_dump_path(db_info.database_name, ''))
        cmd = cmd_format.format(path_exec=path_exec,
                                host=db_info.host,
                                port=db_info.port,
                                user=db_info.username,
                                authentication_database=db_info.authentication_database,
                                database=db_info.database_name,
                                password=db_info.password,
                                dump_path=dump_path)
        out, err = shell.exec(cmd)
        try:
            zip_file = file_utils.get_name_without_extension(dump_path) + '.zip'
            file_utils.zip_file(dump_path, zip_file, True)
            out.append(bytes('dump_path:' + zip_file, 'utf-8'))
        except Exception as e:
            out.append(e.__str__())
        return out
    except Exception as e:
        log.error(e)


def restore(db_info: BackupInfo):
    try:
        # /home/vinhn/Downloads/mongodb-database-tools-ubuntu1804-x86_64-100.7.1/bin/mongorestore
        # --host=172.18.101.75
        # --port=27017
        # --username=root
        # --password=123456
        # --authenticationDatabase=admin
        # --drop
        # --nsInclude="kotei_shisan.*" /var/www/backup_db/kotei_shisan/2023.05.29/
        cmd_format = "{path_exec}  " \
                     "--host={host} " \
                     "--port={port}  " \
                     "--username={user} " \
                     "--password={password} " \
                     "--authenticationDatabase={authentication_database} " \
                     "--drop " \
                     "--nsInclude=\"{nsInclude}\" " \
                     "{dump_path}"
        path_exec = database_utils.choose_exec_dump_path(db_info)
        resource_utils.download_third_party_resource(path_exec)
        # path_exec = os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongodump.exe")
        dump_path = os.path.join(db_info.dump_dir, database_utils.generate_dump_path(db_info.database_name, ''))
        cmd = cmd_format.format(path_exec=path_exec,
                                host=db_info.host,
                                port=db_info.port,
                                user=db_info.username,
                                password=db_info.password,
                                authentication_database=db_info.authentication_database,
                                nsInclude=db_info.database_name,
                                dump_path=dump_path)
        out, err = shell.exec(cmd)

        zip_file = file_utils.get_name_without_extension(dump_path) + '.zip'
        file_utils.zip_file(dump_path, zip_file, True)

        out.append(bytes('dump_path:' + dump_path, 'utf-8'))
        return out
    except Exception as e:
        log.error(e)
