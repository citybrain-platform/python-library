# Citybrain Platform Python Library

The Citybrain Platform Python Library provides convenient access to the Citybrain Platform API from applications written in the Python language.

## installation

If you just want to use the package, just run:

```sh
pip install --upgrade citybrain-platform
```

## Usage

The library needs to be configured with your account's secret key which is available on [citybrain.org](https://citybrain.org/#/settings). Either set it as the `CITYBRAIN_APIKEY` environment variable before using the library:

```sh
export CITYBRAIN_APIKEY='...'
```

Or set `citybrain_platform.api_key` to its value:

```python
import citybrain_platform

citybrain_platform.api_key = "..."
```

## Example Code

Examples of how to use this Python library to accomplish various tasks.

### Table Operations

#### Create Table

```python
import citybrain_platform
from citybrain_platform.computing.data_types import Column, ColumnType

columns = [
    Column("col_str", ColumnType.STRING, "this is a comment"),
    Column("col_id", ColumnType.BIGINT),
]

partition_columns = [
    Column("col_pt", ColumnType.INT, "a column for partitioning")
]

ok = citybrain_platform.Computing.create_table(name="test_tbl", columns=columns, partition_columns=partition_columns)
print(ok)
```

#### Get Table Schema

```python
import citybrain_platform

schema = citybrain_platform.Computing.get_table_schema(name="test_tbl")
print(schema)
```

#### Upload Table Data

```python
import citybrain_platform

result = citybrain_platform.Computing.upload_table_data(name="test_tbl", append=True, csv_filepath="aa.csv", partition_key={"col_pt": "19"})
print(result)
```

#### Truncate Table

```python
import citybrain_platform

result = citybrain_platform.Computing.truncate_table(name="test_tbl", partition_key={"col_pt": "19"})
print(result)
```

#### Drop Table

```python
import citybrain_platform

result = citybrain_platform.Computing.drop_table(name="test_tbl")
print(result)
```

#### Make Table Public To Others

```python
import citybrain_platform

public_table_name = citybrain_platform.Computing.public_table(name="test_tbl")
print(public_table_name)
```

#### List Available Tables

```python
import citybrain_platform

tables = citybrain_platform.Computing.list_tables()
print(tables)
```

### Job Operations

#### Create Job

```python
import citybrain_platform

job_id = citybrain_platform.Computing.create_job(sql="select col_str from test_tbl limit 12;")
print(job_id)
```

#### Get Job Status

```python
import citybrain_platform

job_status = citybrain_platform.Computing.get_job_status(job_id="...")
print(job_status)
```

#### Stop Running Job

```python
import citybrain_platform

result = citybrain_platform.Computing.stop_job(job_id="...")
print(result)
```


#### Download Terminated Job Results

```python
import citybrain_platform

citybrain_platform.Computing.get_job_results(job_id="...", filepath="results.csv")
```
