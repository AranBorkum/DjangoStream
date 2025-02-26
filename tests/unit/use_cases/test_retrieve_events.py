import pytest

from django_stream import exceptions
from django_stream.core import use_cases


class TestRetrieveEvents:
    def test_success(self, retrieve_event_use_case: use_cases.RetrieveEvents) -> None:
        retrieve_event_use_case(queue="queue")

    def test_sqs_client_failure(
        self, retrieve_events_client_failure_use_case: use_cases.RetrieveEvents
    ) -> None:
        with pytest.raises(exceptions.FailureToCommunicateWithAwsSqs):
            retrieve_events_client_failure_use_case(queue="queue")
