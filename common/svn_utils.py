import copy
import os

from dotenv import load_dotenv


from beans.result_object import ResultObject
from beans.svn_info import SvnInfo
from beans.svn_status_object import SvnStatusObject
from common import file_utils, log
from entity.backup_info import BackupInfo
import common.shell_exec as shell
from enum_class.status import Status
from enum_class.svn_status import SvnStatus


class SvnUtils:
    load_dotenv()

    # def svn_login(realm, username, may_save):
    #     return True, svn_login_name, svn_login_password, False

    # os.getenv('SLACK_TOKEN')

    # client.callback_get_login = svn_login

    @staticmethod
    def check_out(db_info: BackupInfo):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            checkout_cmd_format = "{path_exec} " \
                                  "--username {username} " \
                                  "--password {password} " \
                                  "checkout " \
                                  "{url} " \
                                  "{path}"
            cmd = checkout_cmd_format.format(path_exec=path_exec,
                                             username=db_info.svn_username,
                                             password=db_info.svn_password,
                                             url=db_info.svn_url,
                                             path=shell.format_path_cmd(db_info.dump_dir),
                                             )
            out, err = shell.exec(cmd)
            result = shell.read_completed_process(out, err)
            data = copy.deepcopy(result.data)
            for re in data:
                if re.strip().endswith("doesn't exist"):
                    SvnUtils.mkdir(db_info)
                    check_out = SvnUtils.check_out(db_info)
                    return check_out

            return result
        except Exception as e:
            log.error(e)

    @staticmethod
    def mkdir(db_info: BackupInfo):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            checkout_cmd_format = "{path_exec} " \
                                  "mkdir -m \"{message}\" " \
                                  "{url} " \
                                  "--username {username} " \
                                  "--password {password} "

            cmd = checkout_cmd_format.format(path_exec=path_exec,
                                             username=db_info.svn_username,
                                             password=db_info.svn_password,
                                             message="Making a new dir.",
                                             url=db_info.svn_url)
            out, err = shell.exec(cmd)
            return shell.read_completed_process(out, err)
        except Exception as e:
            log.error(e)

    @staticmethod
    def update(db_info: BackupInfo, path: str):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            path = shell.format_path_cmd(path)
            checkout_cmd_format = "{path_exec} " \
                                  "update " \
                                  "{path} " \
                                  "--username {username} " \
                                  "--password {password} "
            cmd = checkout_cmd_format.format(path_exec=path_exec,
                                             path=path,
                                             username=db_info.svn_username,
                                             password=db_info.svn_password,
                                             )
            out, err = shell.exec(cmd)
            return out, err
        except Exception as e:
            log.error(e)

    @staticmethod
    def add(path: str):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            path_tmp = shell.format_path_cmd(path)
            cmd_format = "{path_exec} " \
                         "add " \
                         "{path} "
            cmd = cmd_format.format(path_exec=path_exec,
                                    path=path_tmp)
            # cmd = path_exec + " add " + path_tmp
            out, err = shell.exec(cmd)
            return out, err
        except Exception as e:
            log.error(e)

    @staticmethod
    def delete(path: str):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            path = shell.format_path_cmd(path)
            cmd_format = '{path_exec} ' \
                         'delete ' \
                         "{path} "
            cmd = cmd_format.format(path_exec=path_exec,
                                    path=path)
            out, err = shell.exec(cmd)
            return out, err
        except Exception as e:
            log.error(e)

    @staticmethod
    def commit(db_info: BackupInfo, path: str, message: str):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            path = shell.format_path_cmd(path)
            cmd_format = '{path_exec} ' \
                         'commit ' \
                         '--message "{message}" ' \
                         "{path} " \
                         "--username {username} " \
                         "--password {password} "
            cmd = cmd_format.format(path_exec=path_exec,
                                    message=message,
                                    path=path,
                                    username=db_info.svn_username,
                                    password=db_info.svn_password)
            out, err = shell.exec(cmd)
            return out, err
        except Exception as e:
            log.error(e)

    @staticmethod
    def commit_dir(db_info: BackupInfo):
        try:
            svn_status = SvnUtils.status(db_info, db_info.dump_dir)
            res = []
            diff = False
            for svn in svn_status:
                if svn.status == SvnStatus.modified \
                        or svn.status == SvnStatus.added:
                    diff = True
                    # res, out = SvnUtils.commit(svn.path, "svn.path")
                elif svn.status == SvnStatus.deleted:
                    out, err = SvnUtils.delete(svn.path)
                    deleted = shell.read_completed_process(out, err)
                    print(deleted.data)
                    log.info(deleted.data)
                    # res += copy.deepcopy(deleted.data)
                    diff = True
                elif svn.status == SvnStatus.non_version:
                    out, err = SvnUtils.add(svn.path)
                    non_version = shell.read_completed_process(out, err)
                    print(non_version.data)
                    log.info(non_version.data)
                    diff = True
                    # res += copy.deepcopy(non_version.data)
                if diff:
                    out, err = SvnUtils.commit(db_info, str(file_utils.get_parent_path(svn.path)), "commit")
                    tmp = shell.read_completed_process(out, err)
                    res += copy.deepcopy(tmp.data)
            return ResultObject(Status.OK, res, res)
        except Exception as e:
            log.error(e)
            return ResultObject(Status.ERROR, "ERROR", e)

    @staticmethod
    def status(db_info: BackupInfo, path: str):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            path = shell.format_path_cmd(path)
            cmd_format = "{path_exec} " \
                         "status " \
                         "{path} " \
                         "--username {username} " \
                         "--password {password} "
            cmd = cmd_format.format(path_exec=path_exec,
                                    path=path,
                                    username=db_info.svn_username,
                                    password=db_info.svn_password)
            out, err = shell.exec(cmd)
            tmp = shell.read_completed_process(out, err)
            res_arr = []
            if tmp.status == Status.OK:
                for svn in tmp.data:
                    # switcher = {
                    #     SvnStatus.added: '',
                    #     Platform.Windows_32: '',
                    #     Platform.Linux_32: '',
                    #     Platform.Linux_64: '',
                    # }
                    status_char = str(svn)[0]
                    status = SvnStatus.get_item(status_char)
                    svn_obj = SvnStatusObject(status, str(svn)[1:].strip())
                    res_arr.append(svn_obj)
            return res_arr
        except Exception as e:
            log.error(e)

    @staticmethod
    def info(db_info: BackupInfo, path: str):
        try:
            svn_path = os.getenv('SVN_BINARY_PATH')
            path_exec = shell.format_path_cmd(svn_path)
            path = shell.format_path_cmd(path)
            cmd_format = "{path_exec} " \
                         "info " \
                         "{path} " \
                         "--username {username} " \
                         "--password {password} "
            cmd = cmd_format.format(path_exec=path_exec,
                                    path=path,
                                    username=db_info.svn_username,
                                    password=db_info.svn_password)
            out, err = shell.exec(cmd)
            tmp = shell.read_completed_process(out, err)
            info = SvnInfo
            if tmp.status == Status.OK:
                for svn in tmp.data:
                    t_var = svn.split(':')[0]
                    v_var = svn[len(t_var) + 1:].strip()
                    match t_var:
                        case 'Path':
                            info.path = v_var
                        case 'Name':
                            info.name = v_var
                        case 'Working Copy Root Path':
                            info.working_copy_root_path = v_var
                        case 'URL':
                            info.url = v_var
                        case 'Relative URL':
                            info.relative_url = v_var
                        case 'Repository Root':
                            info.repository_root = v_var
                        case 'Repository UUID':
                            info.repository_uuid = v_var
                        case 'Revision UUID':
                            info.revision = v_var
                        case 'Node Kind':
                            info.node_kind = v_var
                        case 'Schedule':
                            info.schedule = v_var
                        case 'Last Changed Author':
                            info.last_changed_author = v_var
                        case 'Last Changed Rev':
                            info.last_changed_rev = v_var
                        case 'Last Changed Date':
                            info.last_changed_date = v_var
                        case 'Text Last Updated':
                            info.text_last_updated = v_var
                        case 'Checksum':
                            info.checksum = v_var
                        # case _:
                        #     print("The language doesn't matter, what matters is solving problems.")
                    # info[t_var] = v_var
                    # res_arr.append(svn_obj)
            return info
        except Exception as e:
            log.error(e)
