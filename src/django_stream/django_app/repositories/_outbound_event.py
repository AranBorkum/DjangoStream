import datetime
import uuid
from typing import Any

from django_stream.core import entities, repositories
from django_stream.django_app import models


class OutboundEventRepository(repositories.EventRepository):
    def persist(
        self,
        event_type: str,
        payload: dict[str, Any],
        queue: str,
        timestamp: datetime.datetime,
        trace_id: uuid.UUID,
        event_id: uuid.UUID | None = None,
    ) -> entities.Event:
        message_data = {
            "type": event_type,
            "payload": payload,
            "queue": queue,
            "trace_id": trace_id,
            "timestamp": timestamp,
        }
        if event_id:
            message_data.update({"id": str(event_id)})

        outbound_message_model = models.OutboundEventModel.objects.create(
            **message_data
        )
        return entities.Event(
            id_=outbound_message_model.id,
            created_at=outbound_message_model.created_at,
            updated_at=outbound_message_model.updated_at,
            event_type=outbound_message_model.type,
            payload=outbound_message_model.payload,
            queue=outbound_message_model.queue,
            trace_id=outbound_message_model.trace_id,
            status=outbound_message_model.status,
            timestamp=outbound_message_model.timestamp,
        )

    def get(self, event_id: uuid.UUID) -> entities.Event:
        outbound_message_model = models.OutboundEventModel.objects.get(id=event_id)
        return entities.Event(
            id_=outbound_message_model.id,
            created_at=outbound_message_model.created_at,
            updated_at=outbound_message_model.updated_at,
            event_type=outbound_message_model.type,
            payload=outbound_message_model.payload,
            queue=outbound_message_model.queue,
            trace_id=outbound_message_model.trace_id,
            status=outbound_message_model.status,
            timestamp=outbound_message_model.timestamp,
        )

    def exists(self, event_id: uuid.UUID) -> bool:
        exists: bool = models.OutboundEventModel.objects.filter(id=event_id).exists()
        return exists

    def set_status(self, event_id: uuid.UUID, status: str) -> entities.Event:
        outbound_message_model = (
            models.OutboundEventModel.objects.select_for_update().get(id=event_id)
        )
        outbound_message_model.status = status
        outbound_message_model.save()
        return entities.Event(
            id_=outbound_message_model.id,
            created_at=outbound_message_model.created_at,
            updated_at=outbound_message_model.updated_at,
            event_type=outbound_message_model.type,
            payload=outbound_message_model.payload,
            queue=outbound_message_model.queue,
            trace_id=outbound_message_model.trace_id,
            status=outbound_message_model.status,
            timestamp=outbound_message_model.timestamp,
        )
