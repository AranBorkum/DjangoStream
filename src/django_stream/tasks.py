import datetime
import json
import logging
import typing

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from django_stream import constants, entities, usecases

logger = logging.getLogger(__name__)


@shared_task(  # type: ignore[untyped-decorator]
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
    acks_late=True,
)
def process_event(self: typing.Any, event: dict[str, typing.Any]) -> None:
    """
    Idempotent SQS-backed Celery task.
    """
    try:
        payload = json.loads(event["body"])
        event_entity = entities.Event(
            id=event["id"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            payload=payload["payload"],
            event_type=payload["event_type"],
            queue=payload["queue"],
            trace_id=event["trace_id"],
            status=constants.InboundEventStatus.PENDING,
            timestamp=datetime.datetime.fromisoformat(event["timestamp"]),
        )
        usecase = usecases.ProcessInboundEvent()
        usecase.process(event=event_entity)

    except SoftTimeLimitExceeded:
        logger.warning("Soft time limit exceeded for %s", event)
        raise

    except Exception as exc:
        logger.exception("Task failed, retrying")
        raise exc
