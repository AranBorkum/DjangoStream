import uuid
from typing import Any

import pytest

from django_stream.core import constants
from django_stream.django_app import models


@pytest.fixture
def inbound_test_event_model(
    event_id: uuid.UUID, trace_id: uuid.UUID, test_event_payload: dict[str, Any]
) -> models.InboundEventModel:
    return models.InboundEventModel.objects.create(
        id=event_id,
        trace_id=trace_id,
        payload=test_event_payload,
        type=constants.EventType.TEST_EVENT,
        queue="queue",
    )
