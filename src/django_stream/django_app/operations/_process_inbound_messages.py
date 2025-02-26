import json
from typing import Any

from django.db import transaction

from django_stream.core import types
from django_stream.django_app import registers


@transaction.atomic
def _process_single_entry(
    sqs_client: types.SQSClient, message: dict[str, Any], queue_url: str
) -> None:
    as_dict = json.loads(message["Body"])
    as_dict.update({"id": message["MessageId"]})
    serializer = registers.serializers.get(key=as_dict["event_type"])(
        data=as_dict,
    )
    if serializer.is_valid(raise_exception=True):
        event = serializer.persist()
        handler = registers.handlers.get(key=event.event_type)()
        handler(event)

    transaction.on_commit(
        lambda: sqs_client.delete_message(
            QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
        )
    )


def process_inbound_messages(
    sqs_client: types.SQSClient, retrieve_response: dict[str, Any], queue_url: str
) -> None:
    if "Messages" not in retrieve_response:
        return

    for message in retrieve_response["Messages"]:
        try:
            _process_single_entry(sqs_client, message, queue_url)
        except Exception as exception:
            print(exception)
