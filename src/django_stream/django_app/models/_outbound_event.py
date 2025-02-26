from django.db import models

from django_stream.core import constants, entities
from django_stream.django_app.models._base import EventModel


class OutboundEventStatus(models.TextChoices):
    PENDING = constants.OutboundEventStatus.PENDING
    PUBLISHED = constants.OutboundEventStatus.PUBLISHED
    FAILED = constants.OutboundEventStatus.FAILED


class OutboundEventModel(EventModel):
    status = models.CharField(
        choices=OutboundEventStatus.choices,
        default=OutboundEventStatus.PENDING,
        max_length=255,
    )

    class Meta:
        db_table = "events_outbound"

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
