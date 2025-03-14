import datetime
import uuid
from typing import Any

import pytest
from django.utils import timezone

from django_stream.core import constants, entities, repositories


@pytest.fixture
def outbound_event_repository(
    event_entity: entities.Event,
) -> repositories.EventRepository:
    class MockOutboundEventRepository(repositories.EventRepository):
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
                id_=event_id or uuid.uuid4(),
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
            new_entity = event_entity
            new_entity.status = status
            return new_entity

    return MockOutboundEventRepository()
