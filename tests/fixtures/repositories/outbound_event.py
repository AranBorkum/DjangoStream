import dataclasses
import datetime
import uuid
from typing import Any

import pytest
from django.utils import timezone

from django_stream import constants, entities, repository_interfaces


@pytest.fixture
def outbound_event_repository(
    event_entity: entities.Event,
) -> repository_interfaces.EventRepository:
    class MockOutboundEventRepository(repository_interfaces.EventRepository):
        def persist(
            self,
            event_type: str,
            payload: dict[str, Any],
            queue: str,
            timestamp: datetime.datetime,
            trace_id: uuid.UUID,
            event_id: uuid.UUID | None = None,
        ) -> entities.Event:
            return entities.Event(
                id=event_id or uuid.uuid4(),
                created_at=timezone.now(),
                updated_at=timezone.now(),
                payload=payload,
                event_type=event_type,
                queue=queue,
                status=constants.OutboundEventStatus.PENDING,
                trace_id=trace_id,
                timestamp=timezone.now(),
            )

        def get(self, event_id: uuid.UUID) -> entities.Event:
            return event_entity

        def exists(self, event_id: uuid.UUID) -> bool:
            return False

        def set_status(self, event_id: uuid.UUID, status: str) -> entities.Event:
            entity_as_dict = dataclasses.asdict(event_entity)
            entity_as_dict.update({"status": status})
            return entities.Event(**entity_as_dict)

    return MockOutboundEventRepository()
