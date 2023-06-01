import sys
import os

from shellingham._core import SHELL_NAMES

from enum_class.platform import Platform
import shellingham


def shell_detector():
    try:
        shell = shellingham.detect_shell()
        return shell
    except shellingham.ShellDetectionFailure:
        shell = provide_default()
        name = os.path.basename(shell).lower()
        name_split = name.split('.')
        if name in SHELL_NAMES:
            return (name, shell)
        elif name_split[0] in SHELL_NAMES:
            return (name_split[0], shell)


def provide_default():
    if os.name == 'posix':
        return os.environ['SHELL']
    elif os.name == 'nt':
        return os.environ['COMSPEC']
    raise NotImplementedError(f'OS {os.name!r} support not available')


def platform_detector():
    platform = sys.platform
    os_name = os.name
    b_64: bool = sys.maxsize > 2 ** 32
    if platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
        if b_64:
            return Platform.Linux_64
        else:
            return Platform.Linux_32
    elif platform == "darwin":
        return Platform.MacOS
    elif os_name == "nt":
        if b_64:
            return Platform.Windows_64
        else:
            return Platform.Windows_32



