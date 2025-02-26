import json
import uuid
from typing import Any

import pytest


@pytest.fixture
def receive_message_response(
    event_id: uuid.UUID, retrieve_event_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "Messages": [
            {
                "MessageId": str(event_id),
                "ReceiptHandle": "receipt_handle",
                "MD5OfBody": "",
                "Body": json.dumps(retrieve_event_payload),
                "Attributes": {},
                "MD5OfMessageAttributes": "",
                "MessageAttributes": {},
            },
        ]
    }


@pytest.fixture
def receive_message_invalid_body_response(event_id: uuid.UUID) -> dict[str, Any]:
    return {
        "Messages": [
            {
                "MessageId": str(event_id),
                "ReceiptHandle": "receipt_handle",
                "MD5OfBody": "",
                "Body": "",
                "Attributes": {},
                "MD5OfMessageAttributes": "",
                "MessageAttributes": {},
            },
        ]
    }


@pytest.fixture
def receive_message_no_message_response() -> dict[str, Any]:
    return {"Messages": []}
