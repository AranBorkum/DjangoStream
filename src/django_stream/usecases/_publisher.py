import abc
import datetime
import typing
import uuid

from django.db import transaction

from django_stream import constants, repository_interfaces


class Publisher(abc.ABC):
    def __init__(self, repository: repository_interfaces.EventRepository) -> None:
        self._repository = repository

    def _mark_as_handled(self, event_id: uuid.UUID) -> None:
        self._repository.set_status(
            event_id=event_id, status=constants.OutboundEventStatus.PUBLISHED
        )

    @abc.abstractmethod
    @transaction.atomic
    def publish(
        self,
        event_type: constants.EventType,
        payload: dict[str, typing.Any],
        queue: str,
        trace_id: uuid.UUID,
        timestamp: datetime.datetime,
    ) -> None: ...
