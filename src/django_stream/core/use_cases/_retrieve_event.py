import logging
from collections.abc import Callable
from typing import Any

from django_stream import exceptions
from django_stream.core import types

logger = logging.getLogger(__name__)


type TOperation = Callable[[types.SQSClient, dict[str, Any], str], None]


class RetrieveEvents:
    def __init__(
        self,
        client: types.SQSClient,
        operation: TOperation,
    ) -> None:
        self._client = client
        self._operation = operation

    def __call__(self, queue: str) -> None:
        queue_url, retrieve_response = self._get_queue_url_and_message_response(
            queue=queue
        )
        self._operation(self._client, retrieve_response, queue_url)

    def _get_queue_url_and_message_response(
        self, queue: str
    ) -> tuple[str, dict[str, Any]]:
        try:
            queue_url = self._client.get_queue_url(QueueName=queue)["QueueUrl"]
            retrieve_response = self._client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=5,  # Can fetch up to 10 messages at a time
                WaitTimeSeconds=10,  # Long polling (reduces empty responses)
                MessageAttributeNames=["All"],  # Fetch all attributes if needed
            )
            return queue_url, retrieve_response
        except Exception as exception:
            raise exceptions.FailureToCommunicateWithAwsSqs from exception
