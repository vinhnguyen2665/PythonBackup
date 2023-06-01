from typing import Any


class SvnInfo:
    path: str
    name: str
    working_copy_root_path: str
    url: str
    relative_url: str
    repository_root: str
    repository_uuid: str
    revision: str
    node_kind: str
    schedule: str
    last_changed: str
    last_changed_rev: str
    last_changed_author: str
    last_changed_date: str
    text_last_updated: str
    checksum: str

    def __new__(cls) -> Any:
        return super().__new__(cls)


