import argparse
from typing import Any

import boto3
from django.core.management import BaseCommand

from django_stream.core import constants, use_cases
from django_stream.django_app import operations


class Command(BaseCommand):
    help = "Updates the assessments records in a SubBatch"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--queue", type=str, required=True)

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        queue = str(kwargs["queue"])
        client = boto3.client(constants.AWSClient.SQS)
        retrieve_events = use_cases.RetrieveEvents(
            client=client,
            operation=operations.process_inbound_messages,
        )
        retrieve_events(queue=queue)
