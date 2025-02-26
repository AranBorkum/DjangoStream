import uuid
from typing import Any

import pytest
from django import db

from django_stream.core import constants
from django_stream.django_app import models, repositories


class TestOutboundEventRepositoryPersist:
    @pytest.mark.django_db
    def test_persist(
        self,
        event_id: uuid.UUID,
        trace_id: uuid.UUID,
        test_event_payload: dict[str, Any],
    ) -> None:
        assert models.OutboundEventModel.objects.count() == 0
        repositories.OutboundEventRepository().persist(
            event_id=event_id,
            trace_id=trace_id,
            queue="test-queue",
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
        )
        assert models.OutboundEventModel.objects.count() == 1
        model = models.OutboundEventModel.objects.first()
        assert model is not None
        assert model.id == event_id
        assert model.trace_id == trace_id
        assert model.type == constants.EventType.TEST_EVENT
        assert model.queue == "test-queue"
        assert model.payload == test_event_payload

    @pytest.mark.django_db
    def test_persist_without_event_id(
        self, trace_id: uuid.UUID, test_event_payload: dict[str, Any]
    ) -> None:
        assert models.OutboundEventModel.objects.count() == 0
        repositories.OutboundEventRepository().persist(
            trace_id=trace_id,
            queue="test-queue",
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
        )
        assert models.OutboundEventModel.objects.count() == 1
        model = models.OutboundEventModel.objects.first()
        assert model is not None
        assert model.id is not None
        assert model.trace_id == trace_id
        assert model.type == constants.EventType.TEST_EVENT
        assert model.queue == "test-queue"
        assert model.payload == test_event_payload

    @pytest.mark.django_db
    def test_persist_clashing_event_id(
        self,
        event_id: uuid.UUID,
        trace_id: uuid.UUID,
        test_event_payload: dict[str, Any],
    ) -> None:
        assert models.OutboundEventModel.objects.count() == 0
        repositories.OutboundEventRepository().persist(
            event_id=event_id,
            trace_id=trace_id,
            queue="test-queue",
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
        )
        assert models.OutboundEventModel.objects.count() == 1
        with pytest.raises(db.IntegrityError):
            repositories.OutboundEventRepository().persist(
                event_id=event_id,
                trace_id=trace_id,
                queue="test-queue",
                event_type=constants.EventType.TEST_EVENT,
                payload=test_event_payload,
            )


class TestOutboundEventRepositoryGet:
    @pytest.mark.django_db
    def test_get(
        self, outbound_test_event_model: models.OutboundEventModel, event_id: uuid.UUID
    ) -> None:
        event = repositories.OutboundEventRepository().get(event_id=event_id)
        assert event.id == outbound_test_event_model.id
        assert event.trace_id == outbound_test_event_model.trace_id
        assert event.event_type == outbound_test_event_model.type
        assert event.queue == outbound_test_event_model.queue
        assert event.payload == outbound_test_event_model.payload

    @pytest.mark.django_db
    def test_get_not_found(self, event_id: uuid.UUID) -> None:
        with pytest.raises(models.OutboundEventModel.DoesNotExist):
            repositories.OutboundEventRepository().get(event_id=event_id)


class TestOutboundEventRepositoryExists:
    @pytest.mark.django_db
    def test_exists(
        self, outbound_test_event_model: models.OutboundEventModel, event_id: uuid.UUID
    ) -> None:
        assert repositories.OutboundEventRepository().exists(event_id=event_id)

    @pytest.mark.django_db
    def test_not_exists(self, event_id: uuid.UUID) -> None:
        assert not repositories.OutboundEventRepository().exists(event_id=event_id)
