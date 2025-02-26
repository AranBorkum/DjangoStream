from collections.abc import Callable
from typing import Any

import pytest

from django_stream.core import types


@pytest.fixture
def process_inbound_message_operation() -> Callable[
    [types.SQSClient, dict[str, Any], str], None
]:
    def func(
        sqs_client: types.SQSClient, retrieve_response: dict[str, Any], queue_url: str
    ) -> None:
        return None

    return func
