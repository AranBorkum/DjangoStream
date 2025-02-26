import json
from typing import Any

from django_stream.core import entities


class TestEvent:
    def test_event_publishable_event(
        self, event_entity: entities.Event, retrieve_event_payload: dict[str, Any]
    ) -> None:
        assert event_entity.publishable_event
        assert json.loads(event_entity.publishable_event) == retrieve_event_payload
