import uuid
from typing import Any

import pytest
from django.utils import timezone

from django_stream import constants


@pytest.fixture
def test_event_payload() -> dict[str, Any]:
    return {"test": "event"}


@pytest.fixture
def retrieve_event_payload(
    trace_id: uuid.UUID, test_event_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "trace_id": str(trace_id),
        "event_type": constants.EventType.TEST_EVENT,
        "queue": "test-queue",
        "payload": test_event_payload,
        "timestamp": timezone.now().isoformat(),
    }


@pytest.fixture
def retrieve_event_invalid_payload(
    trace_id: uuid.UUID, test_event_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "trace_id": str(trace_id),
        "event_type": constants.EventType.TEST_EVENT,
        "payload": test_event_payload,
        "timestamp": timezone.now().isoformat(),
    }
