import datetime
import json
import uuid
from typing import Any


class Event:
    def __init__(
        self,
        id_: uuid.UUID,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        payload: dict[str, Any],
        event_type: str,
        queue: str,
        trace_id: uuid.UUID,
        status: str,
    ):
        self.id = id_
        self.created_at = created_at
        self.updated_at = updated_at
        self.payload = payload
        self.event_type = event_type
        self.queue = queue
        self.trace_id = trace_id
        self.status = status

    @property
    def publishable_event(self) -> str:
        return json.dumps({
            "event_type": self.event_type,
            "payload": self.payload,
            "queue": self.queue,
            "trace_id": str(self.trace_id),
        })
