from uplink import Body, Consumer, Query, Field, get, inject, json, post, response_handler
from uplink.hooks import TransactionHook

class APIResponseException(Exception):
    pass

class ResponseStreamHook(TransactionHook):
    def audit_request(self, consumer, request_builder):
        request_builder.info["stream"] = True
        return super().audit_request(consumer, request_builder)

_response_stream_hook = ResponseStreamHook()

def handle_json_response(response):
    response.iter_lines()
    if response.headers["Content-Type"].startswith("application/json"):
        body = response.json()
        if body["code"] != 200:
            raise APIResponseException(body["message"])
        return body["data"]
    return response

@response_handler(handle_json_response)
class ComputingClient(Consumer):
    """A Python Client for the Citybrain Computing Platform API."""

    def __init__(self, base_url, api_key):
        super(ComputingClient, self).__init__(base_url=base_url)
        self.session.headers["api_key"] = api_key

    @get("computing/table/detail")
    def table_info(self, name: Query("name")):
        pass

    @post("computing/table/upload")
    def table_upload(self, name: Query("name"), append: Query("append"), partition_key: Query("partition_key"), body: Body):
        pass

    @json
    @post("computing/table/create")
    def table_create(self, name: Field("name"), columns: Field("columns"), partition_columns: Field("partition_columns"), description: Field("description"), storage_filesource: Field("storage_filesource"), storage_filetype: Field("storage_filetype")):
        pass

    @json
    @post("computing/table/truncate")
    def table_truncate(self, name: Field("name"), partition_key: Field("partition_key")):
        pass

    @json
    @post("computing/table/drop")
    def table_drop(self, name: Field("name")):
        pass

    @json
    @post("computing/table/public")
    def update_table_status(self, name: Field("name"), status: Field("status")):
        pass

    @get("computing/table/list")
    def table_list(self):
        pass

    @json
    @post("computing/job/submit")
    def job_submit(self, sql: Field("sql"), worker_limit: Field("worker_limit"), split_size: Field("split_size")):
        pass

    @json
    @post("computing/job/stop")
    def job_stop(self, job_id: Field("job_id")):
        pass

    @get("computing/job/status")
    def job_status(self, job_id: Query("job_id")):
        pass

    @inject(_response_stream_hook)
    @get("computing/job/result")
    def job_result(self, job_id: Query("job_id")):
        pass