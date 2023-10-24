from uplink import Body, Consumer, Field, Query, get, inject, json, post, response_handler
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
class StorageClient(Consumer):
    """A Python Client for the Citybrain Storage Platform API."""

    def __init__(self, base_url, api_key):
        super(StorageClient, self).__init__(base_url=base_url)
        self.session.headers["api_key"] = api_key

    @get("storage/file/list")
    def file_list(self, prefix: Query("prefix"), direct_only: Query("direct_only")):
        pass

    @post("storage/file/upload")
    def file_upload(self, path: Query("path"), body: Body):
        pass

    @json
    @post("storage/file/delete")
    def file_delete(self, path: Field("path")):
        pass

    @inject(_response_stream_hook)
    @get("storage/file/download")
    def file_download(self, path: Query("path")):
        pass