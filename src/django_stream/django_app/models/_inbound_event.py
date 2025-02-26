from django.db import models

from django_stream.core import constants, entities
from django_stream.django_app.models._base import EventModel


class InboundEventStatus(models.TextChoices):
    PENDING = constants.InboundEventStatus.PENDING
    HANDLED = constants.InboundEventStatus.HANDLED
    FAILED = constants.InboundEventStatus.FAILED


class InboundEventModel(EventModel):
    status = models.CharField(
        choices=InboundEventStatus.choices,
        default=InboundEventStatus.PENDING,
        max_length=255,
    )

    class Meta:
        db_table = "events_inbound"

    def to_entity(self) -> entities.Event:
        return entities.Event(
            id_=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            trace_id=self.trace_id,
            payload=self.payload,
            event_type=self.type,
            queue=self.queue,
            status=self.status,
        )
