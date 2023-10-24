from dataclasses import dataclass

@dataclass
class FileListItem:
    key: str
    size: int
    last_modified: str