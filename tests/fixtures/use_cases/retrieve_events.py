from collections.abc import Callable
from typing import Any

import pytest

from django_stream.core import types, use_cases


@pytest.fixture
def retrieve_event_use_case(
    sqs_client: types.SQSClient,
    process_inbound_message_operation: Callable[
        [types.SQSClient, dict[str, Any], str], None
    ],
) -> use_cases.RetrieveEvents:
    return use_cases.RetrieveEvents(
        client=sqs_client,
        operation=process_inbound_message_operation,
    )


@pytest.fixture
def retrieve_events_client_failure_use_case(
    sqs_client_failure: types.SQSClient,
    process_inbound_message_operation: Callable[
        [types.SQSClient, dict[str, Any], str], None
    ],
) -> use_cases.RetrieveEvents:
    return use_cases.RetrieveEvents(
        client=sqs_client_failure,
        operation=process_inbound_message_operation,
    )
