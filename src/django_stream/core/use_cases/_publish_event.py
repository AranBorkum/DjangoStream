import datetime
import uuid
from collections.abc import Callable
from typing import Any

from django_stream.core import entities, repositories, types

type TOperation = Callable[[types.SQSClient, entities.Event], None]


class PublishEvent:
    def __init__(
        self,
        client: types.SQSClient,
        repository: repositories.EventRepository,
        operation: TOperation,
    ):
        self._client = client
        self._repository = repository
        self._operation = operation

    def __call__(
        self,
        event_type: str,
        payload: dict[str, Any],
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
        self._operation(self._client, event)
