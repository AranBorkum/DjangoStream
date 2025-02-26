import pytest

from django_stream.core import constants, types
from django_stream.django_app import models, operations


class TestPublishOutboundMessage:
    @pytest.mark.django_db
    def test_publish_outbound_message(
        self,
        sqs_client: types.SQSClient,
        outbound_test_event_model: models.OutboundEventModel,
    ) -> None:
        event = outbound_test_event_model.to_entity()
        operations.publish_outbound_message(sqs_client, event)
        outbound_test_event_model.refresh_from_db()
        assert (
            outbound_test_event_model.status == constants.OutboundEventStatus.PUBLISHED
        )

    @pytest.mark.django_db
    def test_publish_outbound_message_failure(
        self,
        sqs_client_failure: types.SQSClient,
        outbound_test_event_model: models.OutboundEventModel,
    ) -> None:
        event = outbound_test_event_model.to_entity()
        operations.publish_outbound_message(sqs_client_failure, event)
        outbound_test_event_model.refresh_from_db()
        assert outbound_test_event_model.status == constants.OutboundEventStatus.FAILED
