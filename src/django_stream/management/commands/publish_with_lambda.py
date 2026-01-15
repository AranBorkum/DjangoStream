import argparse
import datetime
import json
import typing
import uuid

from django.core.management.base import BaseCommand, CommandError

from django_stream import constants, repositories, usecases


class Command(BaseCommand):
    help = "Send a raw JSON IoT-style event to the IoT→Lambda→Celery pipeline"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--function-name",
            type=str,
            default="publishToCelerySqsQueue",
            help="Lambda function name",
        )

        parser.add_argument(
            "--async",
            action="store_true",
            help="Invoke Lambda asynchronously (Event invocation)",
        )

        parser.add_argument(
            "--payload",
            type=str,
            help="Optional raw JSON payload",
        )

    def _generate_payload(
        self, options: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        output_payload: dict[str, typing.Any] = {
            "test": "event",
            "device_id": "test-device-001",
            "temperature": 22.7,
            "humidity": 0.55,
        }

        if payload := options["payload"]:
            try:
                output_payload = json.loads(payload)
            except json.JSONDecodeError as exc:
                raise CommandError(f"Invalid JSON payload: {exc}")

        return output_payload

    def _generate_output(
        self, invocation_type: str, response: dict[str, typing.Any]
    ) -> None:
        if invocation_type == "RequestResponse":
            response_payload = response["Payload"].read()
            try:
                decoded = json.loads(response_payload)
            except json.JSONDecodeError:
                decoded = response_payload.decode("utf-8")

            self.stdout.write(
                self.style.SUCCESS(
                    "✅ Lambda invoked successfully\n"
                    f"Response:\n{json.dumps(decoded, indent=2)}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "✅ Lambda invoked asynchronously\n"
                    f"Request ID: {response['ResponseMetadata']['RequestId']}"
                )
            )

    def handle(
        self, *args: tuple[typing.Any, ...], **options: dict[str, typing.Any]
    ) -> None:
        payload = self._generate_payload(options=options)
        invocation_type = (
            constants.LambdaInvocationType.EVENT
            if options["async"]
            else constants.LambdaInvocationType.REQUEST_RESPONSE
        )
        function_name = str(options["function_name"])

        repository = repositories.OutboundEventRepository()
        usecase = usecases.PublishEventWithLambda(
            repository=repository,
            invocation_type=invocation_type,
            function_name=function_name,
        )

        usecase.publish(
            event_type=constants.EventType.TEST_EVENT,
            payload=payload,
            queue="events",
            trace_id=uuid.uuid4(),
            timestamp=datetime.datetime.now(tz=datetime.UTC),
        )

        self._generate_output(
            invocation_type=invocation_type, response=usecase.response
        )
