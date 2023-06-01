import subprocess
import os
import re

from beans.result_object import ResultObject
from common import sys_utils, log
from common.sys_utils import shell_detector
from enum_class.platform import Platform
from enum_class.status import Status


# def exec(command, capture=True):
#     os.system('cmd /k ' + command)


def exec(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = None
    if p.stdout:
        out = p.stdout.readlines()
    err = None
    if p.stderr:
        err = p.stderr.readlines()
    retval = p.wait()
    # return direct_output.decode("utf-8").split('\r\n')
    return out, err


def read_completed_process(shell_out, shell_err=None):
    version = ''
    msg = []
    error = False
    if shell_out:
        # tmp = shell_out.decode("utf-8").splitlines()
        for out in shell_out:
            if out:
                tmp = out.decode("utf-8")
                m = tmp.replace('\n', '').replace('\r\n', '')
                if m.lower().__contains__('error'):
                    error = True
                msg.append(m)
                log.info(m)
                # for o in out:
                #     if o:
                #         tmp = o.decode("utf-8")
                #         msg.append(tmp.replace('\n', '').replace('\r\n', ''))
    if shell_err:
        # tmp = shell_out.decode("utf-8").splitlines()
        for err in shell_err:
            if err:
                tmp = err.decode("utf-8")
                e = tmp.replace('\n', '').replace('\r\n', '')
                msg.append(e)
                log.info(e)
                # for e in err:
                #     tmp = e.decode("utf-8")
                #     msg.append(tmp.replace('\n', '').replace('\r\n', ''))
                #     if e:
                #         tmp = e.decode("utf-8")
                #         msg.append(tmp.replace('\n', '').replace('\r\n', ''))

    if shell_err or error:
        return ResultObject(status=Status.ERROR, message=msg, data=msg)
    else:
        tmp = ResultObject(status=Status.OK, message=msg, data=msg)
        return tmp


def format_path_cmd(path_str: str):
    # svn_path_arr = path_str.split("\\|/")
    svn_path_arr = re.split(r"[\\|/]", path_str)
    path_exec = ''
    # for p in svn_path_arr:
    #     if p.__contains__(" "):
    #         p = "\"" + p + "\""
    #     # path_exec += os.path.join(os.sep, p)
    #     path_exec = os.path.join(path_exec, p)
    for i in range(len(svn_path_arr)):
        p = svn_path_arr[i]
        if p.__contains__(" "):
            # shell = shell_detector()
            # char = ''
            # if shell[0].__eq__('cmd'):
            #     char = '^'
            # elif shell[0].__eq__('powershell') or shell[0].__eq__('v'):
            #     char = '`'
            # space_idx = p.index(" ")
            # p = svn_path_arr[i][:space_idx] + char + svn_path_arr[i][space_idx:]
            p = r'\"' + p + '"'
        if i == 0:
            char = ''
            if sys_utils.platform_detector() == Platform.Windows_64 or sys_utils.platform_detector() == Platform.Windows_32:
                p += os.sep

        else:
            char = os.sep
        # path_exec += os.path.join(os.sep, p)
        # path_exec = os.path.join(path_exec, p)
        path_exec += char + p
    return path_exec
