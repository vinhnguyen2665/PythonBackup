import os
from pathlib import Path


import common.shell_exec as shell
from entity.backup_info import BackupInfo
from common import file_utils, log
from common import database_utils


def get_version(db_info: BackupInfo):
    try:
        cmd_format = "{path_exec}  " \
                     "--host={host} " \
                     "--port={port}  " \
                     "--user=\"{user}\" " \
                     "--password=\"{password}\" " \
                     "--execute=\"select version()\""
        # path_exec = os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x64", "mysql.exe")
        path_exec = database_utils.choose_exec_query_path(db_info)
        cmd = cmd_format.format(path_exec=path_exec,
                                host=db_info.host,
                                port=db_info.port,
                                user=db_info.username,
                                password=db_info.password)
        out, err = shell.exec(cmd)
        return out
    except Exception as e:
        log.error(e)


def dump(db_info: BackupInfo):
    try:
        cmd_format = "{path_exec} " \
                     "--host={host} " \
                     "--port={port} " \
                     "--user=\"{user}\" " \
                     "--password=\"{password}\" " \
                     "--databases \"{database}\" " \
                     "--result-file={dump_path} "
        if db_info.skip_lock_table:
            cmd_format += '--skip-lock-tables '
        if None != db_info.column_statistics:
            cmd_format += '--column_statistics={column_statistics} '

        # no_tablespaces_ver_57 = "5.7.31"
        # no_tablespaces_ver_8 = "8.0.21"
        # try:
        #     db_version = version.parse(db_info.version_name)
        # except Exception as e:
        #     log.error(e)
        #     db_version = db_info.version_name[: len(no_tablespaces_ver_8)]
        #
        # if db_info.version_name and (db_version >= version.parse(no_tablespaces_ver_57) or
        #                              db_version >= version.parse(no_tablespaces_ver_8)):
        #     cmd_format += '--no-tablespaces '
        if db_info.no_table_spaces:
            cmd_format += '--no-tablespaces '

        path_exec = database_utils.choose_exec_dump_path(db_info)
        dump_path = os.path.join(db_info.dump_dir, database_utils.generate_dump_path(db_info.database_name, '.sql'))
        file_utils.if_not_exist_make_dir(Path(dump_path).parent)
        cmd = cmd_format.format(path_exec=path_exec,
                                host=db_info.host,
                                port=db_info.port,
                                user=db_info.username,
                                database=db_info.database_name,
                                password=db_info.password,
                                column_statistics=db_info.column_statistics,
                                dump_path=dump_path)
        out, err = shell.exec(cmd)

        zip_file = file_utils.get_name_without_extension(dump_path) + '.zip'
        file_utils.zip_file(dump_path, zip_file, True)

        out.append(bytes('dump_path:' + zip_file, 'utf-8'))
        return out
    except Exception as e:
        log.error(e)
