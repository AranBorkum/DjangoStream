import pytest

from django_stream.core import constants, entities
from django_stream.django_app import repositories
from django_stream.django_app.base import handler


@pytest.fixture
def base_handler() -> type[handler.Handler]:
    class BaseHandler(handler.Handler):
        _event_repository = repositories.InboundEventRepository()
        _success_status = constants.InboundEventStatus.HANDLED
        _failure_status = constants.InboundEventStatus.FAILED

        def handle(self, event: entities.Event) -> None:
            pass

    return BaseHandler


@pytest.fixture
def base_handler_failure() -> type[handler.Handler]:
    class BaseHandlerFailure(handler.Handler):
        _event_repository = repositories.InboundEventRepository()
        _success_status = constants.InboundEventStatus.HANDLED
        _failure_status = constants.InboundEventStatus.FAILED

        def handle(self, event: entities.Event) -> None:
            raise Exception

    return BaseHandlerFailure


@pytest.fixture
def base_handler_no_repository() -> type[handler.Handler]:
    class BaseHandlerNoRepository(handler.Handler):
        _event_repository = None  # type: ignore[assignment]
        _success_status = constants.InboundEventStatus.HANDLED
        _failure_status = constants.InboundEventStatus.FAILED

        def handle(self, event: entities.Event) -> None:
            raise Exception

    return BaseHandlerNoRepository


@pytest.fixture
def base_handler_no_success_status() -> type[handler.Handler]:
    class BaseHandlerNoSuccessStatus(handler.Handler):
        _event_repository = repositories.InboundEventRepository()
        _success_status = None  # type: ignore[assignment]
        _failure_status = constants.InboundEventStatus.FAILED

        def handle(self, event: entities.Event) -> None:
            raise Exception

    return BaseHandlerNoSuccessStatus


@pytest.fixture
def base_handler_no_failure_status() -> type[handler.Handler]:
    class BaseHandlerNoFailureStatus(handler.Handler):
        _event_repository = repositories.InboundEventRepository()
        _success_status = constants.InboundEventStatus.HANDLED
        _failure_status = None  # type: ignore[assignment]

        def handle(self, event: entities.Event) -> None:
            raise Exception

    return BaseHandlerNoFailureStatus


@pytest.fixture
def base_handler_set_status_fails() -> type[handler.Handler]:
    class BaseHandlerSetStatusFails(handler.Handler):
        _event_repository = repositories.InboundEventRepository()
        _success_status = constants.InboundEventStatus.HANDLED
        _failure_status = constants.InboundEventStatus.FAILED

        def handle(self, event: entities.Event) -> None:
            pass

        def _success(self, event: entities.Event) -> None:
            raise Exception

        def _failure(self, event: entities.Event) -> None:
            raise Exception

    return BaseHandlerSetStatusFails
