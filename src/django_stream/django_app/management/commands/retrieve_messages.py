import argparse
import logging
import time
from typing import Any

import boto3
from django.core.management import BaseCommand

from django_stream.core import constants, use_cases
from django_stream.django_app import operations
from django_stream.utils.graceful_killer import GracefulKiller

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Updates the assessments records in a SubBatch"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--queue", type=str, required=True)

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        queue = str(kwargs["queue"])
        client = boto3.client(constants.AWSClient.SQS)
        logger.info(
            "Pulling messages from event queue",
            extra={
                "queue": queue,
                "client": constants.AWSClient.SQS,
            },
        )

        retrieve_events = use_cases.RetrieveEvents(
            client=client,
            operation=operations.process_inbound_messages,
        )

        killer = GracefulKiller()
        while not killer.kill_now:
            try:
                retrieve_events(queue=queue)
                time.sleep(10)
            except (Exception, KeyboardInterrupt):
                raise
