import os
import uuid
from datetime import UTC, datetime

import boto3
from kombu import Connection, Producer, serialization

# Environment variables
SQS_QUEUE_URL = os.environ["CELERY_QUEUE_URL"]
SQS_QUEUE_NAME = os.environ["CELERY_QUEUE_NAME"]
AWS_REGION = os.environ["AWS_REGION"]
TASK_NAME = os.environ.get("CELERY_TASK_NAME", "django_stream.tasks.process_event")

# boto3 client
sqs_client = boto3.client("sqs", region_name=AWS_REGION)

# Kombu connection (for serialization only)
connection = Connection("sqs://")


def normalize_iot_event(event: dict) -> dict:
    """
    Ensure the event has required fields and generate defaults if missing.
    Celery requires 'id', so we include it here.
    """
    event = event.copy()
    event.setdefault("device_id", "unknown-device")
    event.setdefault("timestamp", datetime.now(UTC).isoformat())
    # Celery expects 'id'
    event.setdefault("id", str(uuid.uuid4()))
    return event


def serialize_task_for_celery(task_name: str, args: list, kwargs: dict | None = None):
    """
    Serialize a Celery task payload using Kombu (JSON serializer).
    Returns (body, content_type, content_encoding)
    """
    if kwargs is None:
        kwargs = {}

    # Kombu JSON serializer for Celery tasks
    content_type, content_encoding, body_str = serialization.dumps(
        [args, kwargs, {}], serializer="json"
    )
    return body_str, content_type, content_encoding or "utf-8"


# def lambda_handler(event, context):
#     # Normalize IoT event (add device_id, timestamp, id)
#     payload = normalize_iot_event(event)
#
#     # Serialize the payload as a Celery task
#     body, content_type, content_encoding = serialize_task_for_celery(
#         TASK_NAME, args=[payload]
#     )
#
#     # Debug: make sure the body is correct
#     print("BODY TO SEND:", repr(body))
#     print("CONTENT TYPE:", content_type)
#     print("CONTENT ENCODING:", content_encoding)
#
#     # Send message to SQS in a Celery-compatible way
#     sqs_client.send_message(
#         QueueUrl=SQS_QUEUE_URL,
#         MessageBody=body,  # Must be the serialized JSON task
#         MessageAttributes={
#             "content-type": {"StringValue": content_type, "DataType": "String"},
#             "content-encoding": {"StringValue": content_encoding, "DataType": "String"},
#             "task": {"StringValue": TASK_NAME, "DataType": "String"},
#             "id": {"StringValue": payload["id"], "DataType": "String"},
#         },
#     )


def lambda_handler(event, context):
    payload = normalize_iot_event(event)

    body_obj = [[payload], {}, {}]  # args, kwargs, empty options
    content_type, content_encoding, body_str = serialization.dumps(
        body_obj, serializer="json"
    )

    connection = Connection("sqs://")
    with connection.channel() as channel:
        producer = Producer(channel)
        producer.publish(
            body_str,  # JSON string
            serializer="raw",  # already serialized
            routing_key=SQS_QUEUE_NAME,  # full SQS queue URL
            declare=[],
            retry=True,
            content_type=content_type,
            content_encoding=content_encoding,
            headers={"task": TASK_NAME, "id": payload["id"]},
        )
    return {
        "status": "ok",
        "task_name": TASK_NAME,
        "payload": payload,
        "task_id": payload["id"],
    }
