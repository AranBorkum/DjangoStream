from rest_framework import serializers as rest_serializers

from django_stream.core import constants
from django_stream.django_app import registers
from django_stream.django_app.base import serializer


@registers.serializers.register(key=constants.EventType.TEST_EVENT.value)
@serializer.event_serializer
class RetrieveEventPayloadSerializer(rest_serializers.Serializer):  # type: ignore [misc]
    test = rest_serializers.CharField(max_length=255)
