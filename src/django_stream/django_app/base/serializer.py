from rest_framework import serializers

from django_stream.core import entities
from django_stream.django_app import repositories


class EventSerializer(serializers.Serializer):  # type: ignore [misc]
    id = serializers.UUIDField()
    trace_id = serializers.UUIDField()
    event_type = serializers.CharField(max_length=255)
    queue = serializers.CharField(max_length=255)

    def persist(self) -> entities.Event:
        raise NotImplementedError()


def event_serializer(cls: type[serializers.Serializer]) -> type[EventSerializer]:
    class NewClass(EventSerializer):
        payload = cls(source="*")

        def persist(self) -> entities.Event:
            repository = repositories.InboundEventRepository()
            event = repository.persist(
                event_id=self.data["id"],
                event_type=self.data["event_type"],
                queue=self.data["queue"],
                payload=self.data["payload"],
                trace_id=self.data["trace_id"],
            )
            return event

    return NewClass
