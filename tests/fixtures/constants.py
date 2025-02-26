import uuid

import pytest

_EVENT_ID = uuid.uuid4()
_TRACE_ID = uuid.uuid4()


@pytest.fixture
def event_id() -> uuid.UUID:
    return _EVENT_ID


@pytest.fixture
def trace_id() -> uuid.UUID:
    return _TRACE_ID
