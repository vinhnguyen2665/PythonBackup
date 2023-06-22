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


def permission_to_string(octal):
    # Convert a 'rwsr-xr-T' format to a decimal value

    result = ""
    value_letters = [(4, "r"), (2, "w"), (1, "x")]
    # Iterate over each of the digits in octal
    for digit in [int(n) for n in str(octal)]:
        # Check for each of the permissions values
        for value, letter in value_letters:
            if digit >= value:
                result += letter
                digit -= value
            else:
                result += '-'
    return result


def permission_to_num(symbolic):
    '''
    Convert symbolic permission notation to numeric notation.
    '''
    perms = {
        '---': '0',
        '--x': '1',
        '-w-': '2',
        '-wx': '3',
        'r--': '4',
        'r-x': '5',
        'rw-': '6',
        'rwx': '7'
    }

    # Trim Lead If It Exists
    if len(symbolic) == 10:
        symbolic = symbolic[1:]

    # Parse Symbolic to Numeric
    x = (symbolic[:-6], symbolic[3:-3], symbolic[6:])
    numeric = perms[x[0]] + perms[x[1]] + perms[x[2]]
    return numeric
