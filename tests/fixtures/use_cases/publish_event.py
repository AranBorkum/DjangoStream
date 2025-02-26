from collections.abc import Callable

import pytest

from django_stream.core import entities, repositories, types, use_cases


@pytest.fixture
def publish_event_use_case(
    sqs_client: types.SQSClient,
    outbound_event_repository: repositories.EventRepository,
    publish_outbound_message_operation: Callable[
        [types.SQSClient, entities.Event], None
    ],
) -> use_cases.PublishEvent:
    return use_cases.PublishEvent(
        client=sqs_client,
        repository=outbound_event_repository,
        operation=publish_outbound_message_operation,
    )


@pytest.fixture
def publish_event_client_failure_use_case(
    sqs_client_failure: types.SQSClient,
    outbound_event_repository: repositories.EventRepository,
    publish_outbound_message_operation: Callable[
        [types.SQSClient, entities.Event], None
    ],
) -> use_cases.PublishEvent:
    return use_cases.PublishEvent(
        client=sqs_client_failure,
        repository=outbound_event_repository,
        operation=publish_outbound_message_operation,
    )
