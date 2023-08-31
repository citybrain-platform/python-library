from uplink import Consumer, Query, get, inject
from uplink.hooks import TransactionHook

class ResponseStreamHook(TransactionHook):
    def audit_request(self, consumer, request_builder):
        request_builder.info["stream"] = True
        return super().audit_request(consumer, request_builder)

_response_stream_hook = ResponseStreamHook()

class DataClient(Consumer):
    """A Python Client for the Citybrain Data Platform API."""

    def __init__(self, base_url, api_key):
        super(DataClient, self).__init__(base_url=base_url)
        self.session.headers["api_key"] = api_key

    @inject(_response_stream_hook)
    @get("data/download")
    def download(self, data_address: Query("data_address")):
        pass
