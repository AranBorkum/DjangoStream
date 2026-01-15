import uuid

from django.db import models


class EventModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trace_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payload = models.JSONField()
    type = models.CharField(max_length=255)
    queue = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True
