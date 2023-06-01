import functools
import logging
import os
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path

from common import log
import requests
import shutil


def temp_name_from_date():
    return datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")[:-3]


def access_permission(path: str, permission: int):
    # Check whether the specified path exists or not
    exist = is_exist(path)
    is_dir = os.path.isdir(path)
    if exist:
        # Create a new directory because it does not exist
        return os.access(path, permission)
    else:
        parent = get_parent_path(path)
        is_parent_exist = is_exist(parent)
        if not is_parent_exist:
            return access_permission(str(get_parent_path(path)), permission)
        else:
            return os.access(parent, permission)


def is_exist(path):
    return os.path.exists(path)


def if_not_exist_make_dir(path):
    # Check whether the specified path exists or not
    is_parent_exist = is_exist(get_parent_path(path))
    if not is_parent_exist:
        if_not_exist_make_dir(get_parent_path(path))
    exist = is_exist(path)
    is_dir = os.path.isdir(path)
    if not exist or not is_dir:
        # Create a new directory because it does not exist
        os.makedirs(path)
        log.info("The new directory is created! " + str(path))


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_file_name_in_path(path):
    return os.path.basename(path)


def get_name_without_extension(name):
    n_arr = name.split('.')
    n_arr.pop(len(n_arr) - 1)
    re = ''
    i = 0
    for n in n_arr:
        re += n
        if i < len(n_arr) - 1:
            re += '.'
        i += 1
    return re


def get_parent_path(path):
    path = Path(path)
    return path.parent.absolute()


def get_parent_name(path):
    path = path.replace("\\", "/")
    tmp = path.split("/")
    return tmp[len(tmp) - 2]


def get_all_file_in_folder_sub_folder(path_dir):
    re = []
    for path, subdirs, files in os.walk(path_dir):
        for name in files:
            p = os.path.join(path, name)
            re.append(p)
    return re


def delete(target: str):
    is_dir = os.path.isdir(target)
    if is_dir:
        sub_dirs = []
        for dir_name, _sub_dirs, files in os.walk(target):
            for filename in files:
                os.remove(os.path.join(dir_name, filename))
            for sub in _sub_dirs:
                sub_dirs.append(os.path.join(dir_name, sub))
        for _dir in sub_dirs:
            if is_exist(_dir):
                os.removedirs(_dir)
        if is_exist(target):
            os.removedirs(target)

    else:
        if os.path.exists(target):
            os.remove(target)
            log.info("remove " + target)


def zip_file(src: str, des: str, delete_src: bool = False):
    zf = ZipFile(des, "w", ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    is_dir = os.path.isdir(src)
    if is_dir:
        for dirname, subdirs, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                log.info('zipping %s as %s' % (os.path.join(dirname, filename), arcname))
                zf.write(absname, arcname)
    else:
        zf.write(src, arcname=os.path.basename(src))
    zf.close()
    if delete_src:
        delete(src)


#
# def zip_file(src: str, des: str, delete_src: bool = False):
#     zf = ZipFile(des, "w", compression=ZIP_DEFLATED, compresslevel=9)
#     is_dir = os.path.isdir(src)
#     if is_dir:
#         for dirname, subdirs, files in os.walk(src):
#             zf.write(dirname)
#             for filename in files:
#                 zf.write(os.path.join(dirname, filename))
#     else:
#         zf.write(src)
#     zf.close()
#     if delete_src:
#         delete(src)

def download_file(url, file):
    if os.path.isdir(file):
        file += url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raw.read = functools.partial(r.raw.read, decode_content=True)
        with open(file, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return file
