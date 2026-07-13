import datetime
import uuid
from typing import Any

from django_stream import entities, models, repository_interfaces


class InboundEventRepository(repository_interfaces.EventRepository):
    def persist(
        self,
        event_type: str,
        payload: dict[str, Any],
        queue: str,
        timestamp: datetime.datetime,
        trace_id: uuid.UUID,
    ) -> entities.Event:
        message_data = {
            "type": event_type,
            "payload": payload,
            "queue": queue,
            "trace_id": trace_id,
            "timestamp": timestamp,
        }

        inbound_message_model = models.InboundEventModel.objects.create(**message_data)
        return entities.Event(
            id=inbound_message_model.id,
            created_at=inbound_message_model.created_at,
            updated_at=inbound_message_model.updated_at,
            event_type=inbound_message_model.type,
            payload=inbound_message_model.payload,
            queue=inbound_message_model.queue,
            trace_id=inbound_message_model.trace_id,
            status=inbound_message_model.status,
            timestamp=inbound_message_model.timestamp,
        )

    def get(self, event_id: uuid.UUID) -> entities.Event:
        inbound_message_model = models.InboundEventModel.objects.get(id=event_id)
        return entities.Event(
            id=inbound_message_model.id,
            created_at=inbound_message_model.created_at,
            updated_at=inbound_message_model.updated_at,
            event_type=inbound_message_model.type,
            payload=inbound_message_model.payload,
            queue=inbound_message_model.queue,
            trace_id=inbound_message_model.trace_id,
            status=inbound_message_model.status,
            timestamp=inbound_message_model.timestamp,
        )

    def exists(self, event_id: uuid.UUID) -> bool:
        exists: bool = models.InboundEventModel.objects.filter(id=event_id).exists()
        return exists

    def set_status(self, event_id: uuid.UUID, status: str) -> entities.Event:
        inbound_message_model = (
            models.InboundEventModel.objects.select_for_update().get(id=event_id)
        )
        inbound_message_model.status = status
        inbound_message_model.save()
        return entities.Event(
            id=inbound_message_model.id,
            created_at=inbound_message_model.created_at,
            updated_at=inbound_message_model.updated_at,
            event_type=inbound_message_model.type,
            payload=inbound_message_model.payload,
            queue=inbound_message_model.queue,
            trace_id=inbound_message_model.trace_id,
            status=inbound_message_model.status,
            timestamp=inbound_message_model.timestamp,
        )
