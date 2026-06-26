from __future__ import annotations

import dataclasses
import datetime
import typing
import uuid

from django_stream import constants, entities, tasks


@dataclasses.dataclass(frozen=True, kw_only=True)
class PublishEventWithSQS:
    repository: Storage

    class Storage(typing.Protocol):
        def persist(
            self,
            event_type: constants.EventType,
            payload: dict[str, typing.Any],
            queue: str,
            timestamp: datetime.datetime,
            trace_id: uuid.UUID,
            event_id: uuid.UUID | None = None,
        ) -> entities.Event: ...

        def set_status(
            self, *, event_id: uuid.UUID, status: constants.OutboundEventStatus
        ) -> entities.Event: ...

    def __call__(
        self,
        event_type: constants.EventType,
        payload: dict[str, typing.Any],
        queue: str,
        trace_id: uuid.UUID,
        timestamp: datetime.datetime,
    ) -> None:
        event = self.repository.persist(
            event_type=event_type,
            payload=payload,
            queue=queue,
            trace_id=trace_id,
            timestamp=timestamp,
        )

        tasks.process_event.delay(event=event.as_serializable_dict)
        self.repository.set_status(
            event_id=event.id, status=constants.OutboundEventStatus.PUBLISHED
        )
