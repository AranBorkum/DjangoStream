import abc
import datetime
import uuid
from typing import Any

from django_stream.core import entities


class EventRepository(abc.ABC):
    @abc.abstractmethod
    def persist(
        self,
        event_type: str,
        payload: dict[str, Any],
        queue: str,
        timestamp: datetime.datetime,
        trace_id: uuid.UUID,
        event_id: uuid.UUID | None = None,
    ) -> entities.Event: ...

    @abc.abstractmethod
    def get(self, event_id: uuid.UUID) -> entities.Event: ...

    @abc.abstractmethod
    def exists(self, event_id: uuid.UUID) -> bool: ...

    @abc.abstractmethod
    def set_status(self, event_id: uuid.UUID, status: str) -> entities.Event: ...
