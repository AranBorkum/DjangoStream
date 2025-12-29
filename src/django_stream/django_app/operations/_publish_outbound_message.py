import logging
from collections.abc import Callable

from django.db import transaction

from django_stream.core import constants, entities, types
from django_stream.django_app import repositories

logger = logging.getLogger(__name__)


@transaction.atomic
def _update_status(event: entities.Event, status: str) -> None:
    repository = repositories.OutboundEventRepository()
    repository.set_status(event_id=event.id, status=status)


def publish_outbound_message(
    sqs_client: types.SQSClient,
    event: entities.Event,
    callback: Callable[[entities.Event, str], None] = _update_status,
) -> None:
    update_status = constants.OutboundEventStatus.PENDING
    try:
        queue_url = sqs_client.get_queue_url(QueueName=event.queue)["QueueUrl"]
        sqs_client.send_message(QueueUrl=queue_url, MessageBody=event.publishable_event)
        update_status = constants.OutboundEventStatus.PUBLISHED
    except Exception:
        update_status = constants.OutboundEventStatus.FAILED
        logger.exception(
            "Error when publishing outbound message",
            extra={
                "event_id": event.id,
                "event_type": event.event_type,
                "queue": event.queue,
                "trace_id": event.trace_id,
            },
        )
    finally:
        callback(event, update_status)
