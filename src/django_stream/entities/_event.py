import dataclasses
import datetime
import typing
import uuid


@dataclasses.dataclass(frozen=True)
class Event:
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    payload: dict[str, typing.Any]
    event_type: str
    queue: str
    trace_id: uuid.UUID
    status: str
    timestamp: datetime.datetime

    @property
    def as_serializable_dict(self) -> dict[str, typing.Any]:
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "payload": self.payload,
            "event_type": self.event_type,
            "queue": self.queue,
            "trace_id": str(self.trace_id),
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
        }
