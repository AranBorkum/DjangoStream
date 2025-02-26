import uuid
from typing import Any

import pytest
from utils import force_run_on_commit_functions

from django_stream.core import constants, types
from django_stream.django_app import models, operations


class TestProcessInboundMessage:
    @pytest.mark.django_db
    def test_process_inbound_message(
        self,
        sqs_client: types.SQSClient,
        receive_message_response: dict[str, Any],
        trace_id: uuid.UUID,
        event_id: uuid.UUID,
        test_event_payload: dict[str, Any],
    ) -> None:
        assert models.InboundEventModel.objects.count() == 0
        assert sqs_client.delete_message_calls == 0  # type: ignore[attr-defined]
        operations.process_inbound_messages(
            sqs_client, receive_message_response, queue_url="queue_url"
        )
        force_run_on_commit_functions()
        assert models.InboundEventModel.objects.count() == 1
        assert sqs_client.delete_message_calls == 1  # type: ignore[attr-defined]

        model = models.InboundEventModel.objects.first()
        assert model is not None
        assert model.id == event_id
        assert model.trace_id == trace_id
        assert model.type == constants.EventType.TEST_EVENT
        assert model.queue == "test-queue"
        assert model.payload == test_event_payload

    @pytest.mark.django_db
    def test_process_inbound_message_with_invalid_payload(
        self,
        sqs_client: types.SQSClient,
        receive_message_invalid_body_response: dict[str, Any],
    ) -> None:
        assert models.InboundEventModel.objects.count() == 0
        assert sqs_client.delete_message_calls == 0  # type: ignore[attr-defined]
        operations.process_inbound_messages(
            sqs_client, receive_message_invalid_body_response, queue_url="queue_url"
        )
        force_run_on_commit_functions()
        assert models.InboundEventModel.objects.count() == 0
        assert sqs_client.delete_message_calls == 0  # type: ignore[attr-defined]

    @pytest.mark.django_db
    def test_empty_messages_return_none(
        self,
        sqs_client: types.SQSClient,
        receive_message_no_message_response: dict[str, Any],
    ) -> None:
        assert models.InboundEventModel.objects.count() == 0
        operations.process_inbound_messages(
            sqs_client=sqs_client,
            retrieve_response=receive_message_no_message_response,
            queue_url="queue_url",
        )
        assert models.InboundEventModel.objects.count() == 0

    @pytest.mark.django_db
    def test_process_existing_message(
        self,
        sqs_client: types.SQSClient,
        inbound_test_event_model: models.InboundEventModel,
        receive_message_response: dict[str, Any],
        trace_id: uuid.UUID,
        event_id: uuid.UUID,
    ) -> None:
        assert models.InboundEventModel.objects.count() == 1
        model = models.InboundEventModel.objects.first()
        assert model is not None

        assert sqs_client.delete_message_calls == 0  # type: ignore[attr-defined]
        operations.process_inbound_messages(
            sqs_client, receive_message_response, queue_url="queue_url"
        )

        assert models.InboundEventModel.objects.count() == 1
        model = models.InboundEventModel.objects.first()
        assert model is not None

        assert sqs_client.delete_message_calls == 0  # type: ignore[attr-defined]
