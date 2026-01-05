import cache_register
from django.apps import AppConfig
from django.conf import settings


class DjangoStreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_stream.django_app"

    def ready(self) -> None:
        cache_register.autodiscover_registers(str(settings.BASE_DIR))
        cache_register.autoregister_registers(str(settings.BASE_DIR))
