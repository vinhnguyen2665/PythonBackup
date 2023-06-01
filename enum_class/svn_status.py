from enum import Enum


class SvnStatus(Enum):

    def __str__(self):
        return str(self.value)

    @staticmethod
    def get_item(val):
        switcher = {
            'M': SvnStatus.modified,
            '!': SvnStatus.deleted,
            'D': SvnStatus.deleted,
            '?': SvnStatus.non_version,
            'A': SvnStatus.added,
        }
        status = switcher.get(val, None)
        return status

    normal = 0
    modified = 1
    read_only = 2
    conflict = 3
    added = 4
    deleted = 5
    ignored = 6
    non_version = 7
