from cache_register import register

from django_stream.base import handler, serializer

serializers = register.Register[serializer.EventSerializer]("serializers")
handlers = register.Register[handler.Handler]("handlers")
