from django.db import transaction

from django_stream import entities, registers
from django_stream.base import handler as base_handler
from django_stream.base import serializer as base_serializer


class ProcessInboundEvent:
    @transaction.atomic
    def process(self, event: entities.Event) -> None:
        serializer: base_serializer.EventSerializer
        serializer = registers.serializers.get(key=event.event_type)(
            data=event.as_serializable_dict,
        )
        if serializer.is_valid(raise_exception=True):
            serialized_event = serializer.persist()
            handler: base_handler.Handler
            handler = registers.handlers.get(key=serialized_event.event_type)()
            handler(serialized_event)
