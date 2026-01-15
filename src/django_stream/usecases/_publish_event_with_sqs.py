import datetime
import typing
import uuid

from django_stream import constants, tasks
from django_stream.usecases._publisher import Publisher


class PublishEventWithSQS(Publisher):
    def publish(
        self,
        event_type: constants.EventType,
        payload: dict[str, typing.Any],
        queue: str,
        trace_id: uuid.UUID,
        timestamp: datetime.datetime,
    ) -> None:
        event = self._repository.persist(
            event_type=event_type,
            payload=payload,
            queue=queue,
            trace_id=trace_id,
            timestamp=timestamp,
        )

        tasks.process_event.delay(event=event.as_serializable_dict)
        self._mark_as_handled(event_id=event.id)
