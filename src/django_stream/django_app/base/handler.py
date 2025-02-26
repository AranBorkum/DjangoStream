import abc
import logging

from django_stream.core import constants, entities
from django_stream.django_app import repositories

logger = logging.getLogger(__name__)


class Handler(abc.ABC):
    _event_repository = repositories.InboundEventRepository()
    _success_status = constants.InboundEventStatus.HANDLED
    _failure_status = constants.InboundEventStatus.FAILED

    def __init__(self) -> None:
        if not self._event_repository:
            raise AttributeError("Event repository not initialized")

        if not self._success_status:
            raise AttributeError("Success status not initialized")

        if not self._failure_status:
            raise AttributeError("Failure status not initialized")

    @abc.abstractmethod
    def handle(self, event: entities.Event) -> None: ...

    def __call__(self, event: entities.Event) -> entities.Event:
        assert self._event_repository
        try:
            self.handle(event)
            self._success(event=event)
        except Exception as exception:
            logger.exception(f"{exception} encountered while handling event")
            self._failure(event=event)
        finally:
            return self._event_repository.get(event_id=event.id)

    def _success(self, event: entities.Event) -> None:
        assert self._success_status and self._event_repository
        self._event_repository.set_status(event.id, self._success_status)

    def _failure(self, event: entities.Event) -> None:
        assert self._failure_status and self._event_repository
        self._event_repository.set_status(event.id, self._failure_status)
