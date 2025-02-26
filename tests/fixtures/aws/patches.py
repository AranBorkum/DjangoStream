from collections.abc import Generator
from unittest.mock import patch

import boto3
import pytest

from django_stream.core import types


@pytest.fixture
def patch_boto3_sqs_client(
    sqs_client: types.SQSClient,
) -> Generator[types.SQSClient, None, None]:
    sqs = patch.object(boto3, "client", return_value=sqs_client).start()
    yield sqs
    sqs.stop()


@pytest.fixture
def patch_boto3_sqs_client_failure(
    sqs_client_failure: types.SQSClient,
) -> Generator[types.SQSClient, None, None]:
    sqs = patch.object(boto3, "client", return_value=sqs_client_failure).start()
    yield sqs
    sqs.stop()
