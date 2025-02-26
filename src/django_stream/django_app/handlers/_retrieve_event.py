import logging

from django_stream.core import constants, entities
from django_stream.django_app import repositories
from django_stream.django_app.base import handler
from django_stream.django_app.registers import handlers

logger = logging.getLogger(__name__)


@handlers.register(key=constants.EventType.TEST_EVENT.value)
class RetrieveEventHandler(handler.Handler):
    _event_repository = repositories.InboundEventRepository()
    _success_status = constants.InboundEventStatus.HANDLED
    _failure_status = constants.InboundEventStatus.FAILED

    def handle(self, event: entities.Event) -> None:
        logger.info("Handled incoming event")
