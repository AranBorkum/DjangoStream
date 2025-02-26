from collections.abc import Callable

import pytest

from django_stream.core import entities, types


@pytest.fixture
def publish_outbound_message_operation() -> Callable[
    [types.SQSClient, entities.Event], None
]:
    def func(sqs_client: types.SQSClient, event: entities.Event) -> None:
        return None

    return func
