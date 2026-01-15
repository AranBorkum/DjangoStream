import datetime
import json
import typing
import uuid

import boto3

from django_stream import constants, repository_interfaces
from django_stream.usecases._publisher import Publisher


class PublishEventWithLambda(Publisher):
    response: dict[str, typing.Any]

    def __init__(
        self,
        invocation_type: constants.LambdaInvocationType,
        function_name: str,
        repository: repository_interfaces.EventRepository,
    ) -> None:
        super().__init__(repository=repository)
        self._invocation_type = invocation_type
        self._function_name = function_name

    def publish(
        self,
        event_type: constants.EventType,
        payload: dict[str, typing.Any],
        queue: str,
        trace_id: uuid.UUID,
        timestamp: datetime.datetime,
    ) -> None:
        lambda_client = boto3.client(constants.AWSClient.LAMBDA)

        event = self._repository.persist(
            event_type=event_type,
            payload=payload,
            queue=queue,
            trace_id=trace_id,
            timestamp=timestamp,
        )

        self.response = lambda_client.invoke(
            FunctionName=self._function_name,
            InvocationType=self._invocation_type,
            Payload=json.dumps(event.as_serializable_dict).encode("utf-8"),
        )
        self._mark_as_handled(event_id=event.id)
