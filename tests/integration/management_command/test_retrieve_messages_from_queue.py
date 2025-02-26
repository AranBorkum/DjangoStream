import uuid
from typing import Any

import pytest
from django.core.management import call_command

from django_stream import exceptions
from django_stream.core import constants, types
from django_stream.django_app import models


class TestRetrieveMessageFromQueue:
    @pytest.mark.django_db
    def test_retrieve_message_from_queue(
        self,
        patch_boto3_sqs_client: types.SQSClient,
        test_event_payload: dict[str, Any],
        event_id: uuid.UUID,
        trace_id: uuid.UUID,
    ) -> None:
        assert models.InboundEventModel.objects.count() == 0
        call_command("retrieve_messages_from_queue", queue="test-queue")
        assert models.InboundEventModel.objects.count() == 1
        model = models.InboundEventModel.objects.first()
        assert model is not None
        assert model.id == event_id
        assert model.trace_id == trace_id
        assert model.type == constants.EventType.TEST_EVENT
        assert model.queue == "test-queue"
        assert model.payload == test_event_payload

    @pytest.mark.django_db
    def test_retrieve_message_from_queue_sqs_error(
        self, patch_boto3_sqs_client_failure: types.SQSClient
    ) -> None:
        assert models.InboundEventModel.objects.count() == 0
        with pytest.raises(exceptions.FailureToCommunicateWithAwsSqs):
            call_command("retrieve_messages_from_queue", queue="test-queue")

        assert models.InboundEventModel.objects.count() == 0
