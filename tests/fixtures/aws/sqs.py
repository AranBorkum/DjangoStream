from typing import Any

import pytest

from django_stream.core import types


@pytest.fixture
def sqs_client(receive_message_response: dict[str, Any]) -> types.SQSClient:
    class Client:
        _delete_message_calls = 0

        def delete_message(self, QueueUrl: str, ReceiptHandle: str) -> None:
            self._delete_message_calls += 1

        def send_message(self, QueueUrl: str, MessageBody: str) -> dict[str, Any]:
            return {}

        def get_queue_url(self, QueueName: str) -> dict[str, Any]:
            return {"QueueUrl": "test-queue"}

        def receive_message(
            self,
            QueueUrl: str,
            MaxNumberOfMessages: int,
            WaitTimeSeconds: int,
            MessageAttributeNames: list[str],
        ) -> dict[str, Any]:
            return receive_message_response

        @property
        def delete_message_calls(self) -> int:
            return self._delete_message_calls

    return Client()


@pytest.fixture
def sqs_client_failure() -> types.SQSClient:
    class ClientFailure:
        def delete_message(self, QueueUrl: str, ReceiptHandle: str) -> None:
            raise

        def send_message(self, QueueUrl: str, MessageBody: str) -> dict[str, Any]:
            raise

        def get_queue_url(self, QueueName: str) -> dict[str, Any]:
            raise

        def receive_message(
            self,
            QueueUrl: str,
            MaxNumberOfMessages: int,
            WaitTimeSeconds: int,
            MessageAttributeNames: list[str],
        ) -> dict[str, Any]:
            raise

    return ClientFailure()
