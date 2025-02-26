import argparse
import uuid
from typing import Any

import boto3
from django.core.management import BaseCommand

from django_stream.core import constants, use_cases
from django_stream.django_app import operations, repositories


class Command(BaseCommand):
    help = "Updates the assessments records in a SubBatch"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--queue", type=str, required=True)

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        queue = str(kwargs["queue"])
        client = boto3.client(constants.AWSClient.SQS)
        repository = repositories.OutboundEventRepository()
        publish_event = use_cases.PublishEvent(
            client=client,
            repository=repository,
            operation=operations.publish_outbound_message,
        )
        publish_event(
            queue=queue,
            event_type=constants.EventType.TEST_EVENT,
            payload={"test": "event"},
            trace_id=uuid.uuid4(),
        )
