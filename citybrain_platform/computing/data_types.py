from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class ColumnType(str, Enum):
    STRING: str = "STRING"
    INT: str = "INT"
    BIGINT: str = "BIGINT"
    FLOAT: str = "FLOAT"
    DOUBLE: str = "DOUBLE"
    TIMESTAMP: str = "TIMESTAMP"

class JobStatus(str, Enum):
    UNSTARTED: str = "unstarted"
    RUNNING: str = "running"
    TERMINATED: str = "terminated"

class ExternalFiletype(str, Enum):
    CSV: str = "csv"
    PARQUET: str = "parquet"

@dataclass
class Column:
    name: str
    type: ColumnType
    comment: str = ""

@dataclass
class Schema:
    name: str
    comment: str
    columns: List[Column]
    partition_columns: List[Column]
    cluster_columns: List[Column]
    create_table_sql: str

@dataclass
class TableListItem:
    name: str
    description: str

@dataclass
class AvaliableTableList:
    public: List[TableListItem]
    own: List[TableListItem]

@dataclass
class JobProgress:
    task_name: str
    total_workers: int
    running_workers: int
    terminated_workers: int

@dataclass
class JobSummary:
    start_time: str
    end_time: str
    job_run_time: int
    cpu_cost: int
    mem_cost: int
    extra: str

@dataclass
class JobStatusInfo:
    status: JobStatus
    progress: List[JobProgress]
    summary: Optional[JobSummary] = None

