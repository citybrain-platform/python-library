from dataclasses import  asdict
import json
from typing import Dict, List
from dacite import from_dict, Config
from citybrain_platform.computing import data_types
from citybrain_platform.computing.client import ComputingClient
import citybrain_platform

__all__ = ["Computing"]

class Computing():
    __CLIENT: ComputingClient = None

    @classmethod
    def __client(cls) -> ComputingClient:
        if getattr(cls, '__CLIENT', None) is None:
            cls.__CLIENT = ComputingClient(base_url=citybrain_platform.api_baseurl, api_key=citybrain_platform.api_key)
        return cls.__CLIENT
    
    @classmethod
    def create_table(cls, name: str, columns: List[data_types.Column], partition_columns: List[data_types.Column] = [], description: str = "", storage_filesource: str = "", storage_filetype: data_types.ExternalFiletype = data_types.ExternalFiletype.CSV) -> bool:
        result = cls.__client().table_create(
            name=name,
            columns=[asdict(col) for col in columns],
            partition_columns=[asdict(col) for col in partition_columns],
            description=description,
            storage_filesource=storage_filesource,
            storage_filetype=storage_filetype.value
        )
        return result

    @classmethod
    def get_table_schema(cls, name: str) -> data_types.Schema:
        result = cls.__client().table_info(name=name)
        table_schema = from_dict(
            data_class=data_types.Schema, 
            data=result,
            config=Config(type_hooks={data_types.ColumnType: data_types.ColumnType}),
        )
        return table_schema
    
    @classmethod
    def upload_table_data(cls, name: str, append: bool, csv_filepath: str, partition_key: Dict[str, str] = None) -> bool:
        appendParam = "true" if append else "false"
        result = False
        with open(csv_filepath, 'rb') as f:
            result = cls.__client().table_upload(name=name, append=appendParam, partition_key=json.dumps(partition_key), body=f)
        return result
    
    @classmethod
    def truncate_table(cls, name: str, partition_key: Dict[str, str] = None) -> bool:
        result = cls.__client().table_truncate(name=name, partition_key=partition_key)
        return result
    
    @classmethod
    def drop_table(cls, name: str) -> bool:
        result = cls.__client().table_drop(name=name)
        return result
    
    @classmethod
    def update_table_status(cls, name: str, public: bool) -> str:
        status = "public" if public else "private"
        result = cls.__client().update_table_status(name=name, status=status)
        return result

    
    @classmethod
    def list_tables(cls) -> data_types.AvaliableTableList:
        result = cls.__client().table_list()
        table_list = from_dict(data_class=data_types.AvaliableTableList, data=result)
        return table_list
    
    @classmethod
    def create_job(cls, sql: str, worker_limit: int = 0, split_size: int = 0) -> str:
        result = cls.__client().job_submit(sql=sql, worker_limit=worker_limit, split_size=worker_limit)
        return result
    
    @classmethod
    def stop_job(cls, job_id: str) -> bool:
        result = cls.__client().job_stop(job_id=job_id)
        return result
    
    @classmethod
    def get_job_status(cls, job_id: str) -> data_types.JobStatusInfo:
        result = cls.__client().job_status(job_id=job_id)
        job_status = from_dict(
            data_class=data_types.JobStatusInfo, 
            data=result, 
            config=Config(type_hooks={data_types.JobStatus: data_types.JobStatus}),
        )

        if job_status.summary != None:
            job_status.summary.cpu_cost /= 100
            job_status.summary.mem_cost /= 100

        return job_status
    
    @classmethod
    def get_job_results(cls, job_id: str, filepath: str):
        response = cls.__client().job_result(job_id=job_id)
        with open(filepath, "wb") as f:
            for l in response.iter_lines():
                f.write(l)
                f.write(b'\n')
