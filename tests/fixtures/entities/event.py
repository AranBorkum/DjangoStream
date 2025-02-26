import uuid
from typing import Any

import pytest
from django.utils import timezone

from django_stream.core import constants, entities


@pytest.fixture
def event_entity(
    event_id: uuid.UUID, trace_id: uuid.UUID, test_event_payload: dict[str, Any]
) -> entities.Event:
    return entities.Event(
        id_=event_id,
        created_at=timezone.now(),
        updated_at=timezone.now(),
        payload=test_event_payload,
        event_type=constants.EventType.TEST_EVENT,
        queue="test-queue",
        trace_id=trace_id,
        status="PENDING",
    )
