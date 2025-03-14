import uuid
from typing import Any

from django.utils import timezone

from django_stream.core import constants, use_cases


class TestPublishEvent:
    def test_success(
        self,
        publish_event_use_case: use_cases.PublishEvent,
        test_event_payload: dict[str, Any],
        trace_id: uuid.UUID,
    ) -> None:
        publish_event_use_case(
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
            queue="test-queue",
            trace_id=trace_id,
            timestamp=timezone.now(),
        )
