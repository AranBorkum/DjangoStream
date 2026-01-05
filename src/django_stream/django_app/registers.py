import cache_register

from django_stream.django_app.base import handler, serializer

serializers = cache_register.Register[serializer.EventSerializer]("serializers")
handlers = cache_register.Register[handler.Handler]("handlers")
