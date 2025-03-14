import uuid
from typing import Any

import pytest
from django import db
from django.utils import timezone

from django_stream.core import constants
from django_stream.django_app import models, repositories


class TestInboundEventRepositoryPersist:
    @pytest.mark.django_db
    def test_persist(
        self,
        event_id: uuid.UUID,
        trace_id: uuid.UUID,
        test_event_payload: dict[str, Any],
    ) -> None:
        assert models.InboundEventModel.objects.count() == 0
        repositories.InboundEventRepository().persist(
            event_id=event_id,
            trace_id=trace_id,
            queue="test-queue",
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
            timestamp=timezone.now(),
        )
        assert models.InboundEventModel.objects.count() == 1
        model = models.InboundEventModel.objects.first()
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
        assert models.InboundEventModel.objects.count() == 0
        repositories.InboundEventRepository().persist(
            trace_id=trace_id,
            queue="test-queue",
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
            timestamp=timezone.now(),
        )
        assert models.InboundEventModel.objects.count() == 1
        model = models.InboundEventModel.objects.first()
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
        assert models.InboundEventModel.objects.count() == 0
        repositories.InboundEventRepository().persist(
            event_id=event_id,
            trace_id=trace_id,
            queue="test-queue",
            event_type=constants.EventType.TEST_EVENT,
            payload=test_event_payload,
            timestamp=timezone.now(),
        )
        assert models.InboundEventModel.objects.count() == 1
        with pytest.raises(db.IntegrityError):
            repositories.InboundEventRepository().persist(
                event_id=event_id,
                trace_id=trace_id,
                queue="test-queue",
                event_type=constants.EventType.TEST_EVENT,
                payload=test_event_payload,
                timestamp=timezone.now(),
            )


class TestInboundEventRepositoryGet:
    @pytest.mark.django_db
    def test_get(
        self, inbound_test_event_model: models.InboundEventModel, event_id: uuid.UUID
    ) -> None:
        event = repositories.InboundEventRepository().get(event_id=event_id)
        assert event.id == inbound_test_event_model.id
        assert event.trace_id == inbound_test_event_model.trace_id
        assert event.event_type == inbound_test_event_model.type
        assert event.queue == inbound_test_event_model.queue
        assert event.payload == inbound_test_event_model.payload

    @pytest.mark.django_db
    def test_get_not_found(self, event_id: uuid.UUID) -> None:
        with pytest.raises(models.InboundEventModel.DoesNotExist):
            repositories.InboundEventRepository().get(event_id=event_id)


class TestInboundEventRepositoryExists:
    @pytest.mark.django_db
    def test_exists(
        self, inbound_test_event_model: models.InboundEventModel, event_id: uuid.UUID
    ) -> None:
        assert repositories.InboundEventRepository().exists(event_id=event_id)

    @pytest.mark.django_db
    def test_not_exists(self, event_id: uuid.UUID) -> None:
        assert not repositories.InboundEventRepository().exists(event_id=event_id)
