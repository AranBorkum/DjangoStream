import dataclasses
import typing

from cache_register import register
from django.db import transaction

from django_stream.base import handler as base_handler
from django_stream.base import serializer as base_serializer


@dataclasses.dataclass(frozen=True, kw_only=True)
class ProcessInbountEvent:
    serializer_register: register.Register[base_serializer.EventSerializer]
    handler_register: register.Register[base_handler.Handler]

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class NoSerializerForEvent(Exception):
        event_type: str

        def __str__(self) -> str:
            return f"No registered serializer for event {self.event_type}"

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class NoHandlerForEvent(Exception):
        event_type: str

        def __str__(self) -> str:
            return f"No registered handler for event {self.event_type}"

    @transaction.atomic
    def __call__(self, event: dict[str, typing.Any]) -> None:
        serializer = self.serializer_register.get(key=event["event_type"])
        if serializer is None:
            raise self.NoSerializerForEvent(event_type=event["event_type"])

        serializer = serializer(data=event)
        serializer.is_valid(raise_exception=True)
        serialized_event = serializer.persist()
        handler = self.handler_register.get(key=serialized_event.event_type)

        if handler is None:
            raise self.NoHandlerForEvent(event_type=event["event_type"])

        handler(event=serialized_event)
