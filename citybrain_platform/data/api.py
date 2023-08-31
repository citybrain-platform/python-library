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