from rest_framework import serializers

from django_stream import entities, repositories


class EventSerializer(serializers.Serializer):  # type: ignore [misc]
    trace_id = serializers.UUIDField()
    event_type = serializers.CharField(max_length=255)
    queue = serializers.CharField(max_length=255)
    timestamp = serializers.DateTimeField()

    def persist(self) -> entities.Event:
        raise NotImplementedError()


def event_serializer(cls: type[serializers.Serializer]) -> type[EventSerializer]:
    class NewClass(EventSerializer):
        payload = cls(source="*")

        def persist(self) -> entities.Event:
            repository = repositories.InboundEventRepository()
            event = repository.persist(
                event_type=self.data["event_type"],
                queue=self.data["queue"],
                payload=self.data["payload"],
                trace_id=self.data["trace_id"],
                timestamp=self.data["timestamp"],
            )
            return event

    return NewClass
