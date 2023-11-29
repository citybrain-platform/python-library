from uplink import Consumer, Field, Query, get, inject, json, post, response_handler
from uplink.hooks import TransactionHook

class ResponseStreamHook(TransactionHook):
    def audit_request(self, consumer, request_builder):
        request_builder.info["stream"] = True
        return super().audit_request(consumer, request_builder)

_response_stream_hook = ResponseStreamHook()

class APIResponseException(Exception):
    pass

def handle_json_response(response):
    response.iter_lines()
    if response.headers["Content-Type"].startswith("application/json"):
        body = response.json()
        if body["code"] != 200:
            raise APIResponseException(body["message"])
        return body["data"]
    return response

@response_handler(handle_json_response)
class DataClient(Consumer):
    """A Python Client for the Citybrain Data Platform API."""

    def __init__(self, base_url, api_key):
        super(DataClient, self).__init__(base_url=base_url)
        self.session.headers["api_key"] = api_key

    @inject(_response_stream_hook)
    @get("data/download")
    def download(self, data_address: Query("data_address")):
        pass

    @json
    @post("data/add_remote")
    def add_remote(self, name: Field("name"), description: Field("description"), url: Field("url")):
        pass

    @json
    @post("data/add_storage")
    def add_storage(self, name: Field("name"), description: Field("description"), file_path: Field("file_path")):
        pass