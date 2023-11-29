__all__ = ["Data"]

import citybrain_platform
from citybrain_platform.data.client import DataClient


class Data():
    __CLIENT: DataClient = None

    @classmethod
    def __client(cls) -> DataClient:
        if getattr(cls, '__CLIENT', None) is None:
            cls.__CLIENT = DataClient(base_url=citybrain_platform.api_baseurl, api_key=citybrain_platform.api_key)
        return cls.__CLIENT
    
    @classmethod
    def download(cls, data_address: str, save_file: str):
        resp = cls.__client().download(data_address=data_address)
        resp.raise_for_status()
        
        with open(save_file, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=4096): 
                f.write(chunk)
    
    @classmethod
    def add_remote(cls, name: str, description: str, remote_url: str) -> str:
        result = cls.__client().add_remote(name=name, description=description, url=remote_url)
        return result

    @classmethod
    def add_storage(cls, name: str, description: str, file_path: str) -> str:
        result = cls.__client().add_storage(name=name, description=description, file_path=file_path)
        return result


        