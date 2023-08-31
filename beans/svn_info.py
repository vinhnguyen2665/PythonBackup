from typing import Any


class SvnInfo:
    path: str | None = None
    name: str | None = None
    working_copy_root_path: str | None = None
    url: str | None = None
    relative_url: str | None = None
    repository_root: str | None = None
    repository_uuid: str | None = None
    revision: str | None = None
    node_kind: str | None = None
    schedule: str | None = None
    last_changed: str | None = None
    last_changed_rev: str | None = None
    last_changed_author: str | None = None
    last_changed_date: str | None = None
    text_last_updated: str | None = None
    checksum: str | None = None

    def __new__(cls) -> Any:
        return super().__new__(cls)


