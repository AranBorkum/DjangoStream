import pytest

from django_stream.core import constants
from django_stream.django_app import models
from django_stream.django_app.base import handler


class TestHandler:
    @pytest.mark.django_db
    def test_handle_event(
        self,
        inbound_test_event_model: models.InboundEventModel,
        base_handler: type[handler.Handler],
    ) -> None:
        event = inbound_test_event_model.to_entity()
        event = base_handler()(event)
        assert event.status == constants.InboundEventStatus.HANDLED

    @pytest.mark.django_db
    def test_handle_event_failure(
        self,
        inbound_test_event_model: models.InboundEventModel,
        base_handler_failure: type[handler.Handler],
    ) -> None:
        event = inbound_test_event_model.to_entity()
        event = base_handler_failure()(event)
        assert event.status == constants.InboundEventStatus.FAILED

    def test_handler_missing_repository(
        self, base_handler_no_repository: type[handler.Handler]
    ) -> None:
        with pytest.raises(AttributeError):
            base_handler_no_repository()

    def test_handler_missing_success_status(
        self, base_handler_no_success_status: type[handler.Handler]
    ) -> None:
        with pytest.raises(AttributeError):
            base_handler_no_success_status()

    def test_handler_missing_failure_status(
        self, base_handler_no_failure_status: type[handler.Handler]
    ) -> None:
        with pytest.raises(AttributeError):
            base_handler_no_failure_status()

    @pytest.mark.django_db
    def test_handle_event_set_status_failure(
        self,
        inbound_test_event_model: models.InboundEventModel,
        base_handler_set_status_fails: type[handler.Handler],
    ) -> None:
        event = inbound_test_event_model.to_entity()
        event = base_handler_set_status_fails()(event)
        assert event.status == constants.InboundEventStatus.PENDING
