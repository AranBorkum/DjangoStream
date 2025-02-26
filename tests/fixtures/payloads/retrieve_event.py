import uuid
from typing import Any

import pytest

from django_stream.core import constants


@pytest.fixture
def test_event_payload() -> dict[str, Any]:
    return {"test": "event"}


@pytest.fixture
def retrieve_event_payload(
    event_id: uuid.UUID, trace_id: uuid.UUID, test_event_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "trace_id": str(trace_id),
        "event_type": constants.EventType.TEST_EVENT,
        "queue": "test-queue",
        "payload": test_event_payload,
    }
