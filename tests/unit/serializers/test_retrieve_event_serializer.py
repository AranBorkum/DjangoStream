import uuid
from typing import Any

from django_stream.django_app import serializers
from django_stream.django_app.registers import serializers as serializer_registers


class TestRetrieveEventSerializer:
    def test_serializer(
        self, event_id: uuid.UUID, retrieve_event_payload: dict[str, Any]
    ) -> None:
        retrieve_event_payload.update({"id": event_id})
        assert serializers.RetrieveEventPayloadSerializer(
            data=retrieve_event_payload
        ).is_valid()

    def test_missing_params(self, retrieve_event_payload: dict[str, Any]) -> None:
        assert not serializers.RetrieveEventPayloadSerializer(
            data=retrieve_event_payload
        ).is_valid()

    def test_serialize_from_register(
        self, event_id: uuid.UUID, retrieve_event_payload: dict[str, Any]
    ) -> None:
        retrieve_event_payload.update({"id": event_id})
        serializer = serializer_registers.get(retrieve_event_payload["event_type"])
        assert serializer(data=retrieve_event_payload).is_valid()
