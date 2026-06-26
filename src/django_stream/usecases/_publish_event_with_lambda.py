from __future__ import annotations

import dataclasses
import datetime
import json
import typing
import uuid

from django_stream import constants, entities


@dataclasses.dataclass(frozen=True, kw_only=True)
class PublishEventWithLambda:
    repository: _Repository
    client: _Client
    invocation_type: constants.LambdaInvocationType
    function_name: str

    class _Repository(typing.Protocol):
        def persist(
            self,
            event_type: constants.EventType,
            payload: dict[str, typing.Any],
            queue: str,
            timestamp: datetime.datetime,
            trace_id: uuid.UUID,
            event_id: uuid.UUID | None = None,
        ) -> entities.Event: ...

        def set_status(
            self, *, event_id: uuid.UUID, status: constants.OutboundEventStatus
        ) -> entities.Event: ...

    class _Client(typing.Protocol):
        def invoke(
            self,
            FunctionName: str,
            InvocationType: constants.LambdaInvocationType,
            Payload: bytes,
        ) -> None: ...

    def __call__(
        self,
        event_type: constants.EventType,
        payload: dict[str, typing.Any],
        queue: str,
        trace_id: uuid.UUID,
        timestamp: datetime.datetime,
    ) -> None:
        event = self.repository.persist(
            event_type=event_type,
            payload=payload,
            queue=queue,
            trace_id=trace_id,
            timestamp=timestamp,
        )

        self.client.invoke(
            FunctionName=self.function_name,
            InvocationType=self.invocation_type,
            Payload=json.dumps(event.as_serializable_dict).encode("utf-8"),
        )
        self.repository.set_status(
            event_id=event.id,
            status=constants.OutboundEventStatus.PUBLISHED,
        )
