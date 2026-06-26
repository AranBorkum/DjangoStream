import logging
import typing

import celery
from celery import exceptions as celery_exceptions

from django_stream import registers, usecases

logger = logging.getLogger(__name__)


@celery.shared_task(  # type: ignore[untyped-decorator]
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
        process_inbound_event = usecases.ProcessInbountEvent(
            serializer_register=registers.serializers,
            handler_register=registers.handlers,
        )
        process_inbound_event(event=event)
    except celery_exceptions.SoftTimeLimitExceeded:
        logger.warning(f"Soft time limit exceeded for {event}")
        raise

    except Exception as exc:
        logger.exception("Task failed, retrying")
        raise exc
