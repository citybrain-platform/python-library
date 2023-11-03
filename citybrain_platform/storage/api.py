from typing import List
from dacite import from_dict
from citybrain_platform.storage import data_types
from citybrain_platform.storage.client import StorageClient
import citybrain_platform

__all__ = ["Storage"]

class Storage():
    __CLIENT: StorageClient = None

    @classmethod
    def __client(cls) -> StorageClient:
        if getattr(cls, '__CLIENT', None) is None:
            cls.__CLIENT = StorageClient(base_url=citybrain_platform.api_baseurl, api_key=citybrain_platform.api_key)
        return cls.__CLIENT
    
    @classmethod
    def upload_file(cls, remote_path: str, local_file: str) -> bool:
        result = False
        with open(local_file, "rb") as f:
            result = cls.__client().file_upload(path=remote_path, body=f)
        return result
    
    @classmethod
    def delete_file(cls, remote_path: str) -> bool:
        return cls.__client().file_delete(path=remote_path)
    
    @classmethod
    def list_files(cls, prefix: str = "", direct_only: bool = False) -> List[data_types.FileListItem]:
        result = cls.__client().file_list(prefix=prefix, direct_only=direct_only)
        table_list = [from_dict(data_class=data_types.FileListItem, data=item) for item in result]
        return table_list
    
    @classmethod
    def download_file(cls, remote_path: str, local_file: str):
        response = cls.__client().file_download(path=remote_path)
        with open(local_file, "wb") as f:
            for l in response.iter_lines():
                f.write(l)
                f.write(b'\n')
