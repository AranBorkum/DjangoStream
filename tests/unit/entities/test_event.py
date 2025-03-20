import json
from typing import Any

from django_stream.core import entities


class TestEvent:
    def test_event_publishable_event(
        self, event_entity: entities.Event, retrieve_event_payload: dict[str, Any]
    ) -> None:
        assert event_entity.publishable_event
        event = json.loads(event_entity.publishable_event)
        assert retrieve_event_payload["trace_id"] == event["trace_id"]
        assert retrieve_event_payload["event_type"] == event["event_type"]
        assert retrieve_event_payload["queue"] == event["queue"]
        assert retrieve_event_payload["payload"] == event["payload"]
