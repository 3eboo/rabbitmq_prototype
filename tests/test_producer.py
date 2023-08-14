from unittest.mock import patch

import pytest

from rabbitmq_prototype.producer.producer import produce_message


@pytest.fixture
def mock_pika():
    with patch('producer.pika') as mock_pika:
        yield mock_pika


def test_produce_message(mock_pika):
    mock_channel = mock_pika.BlockingConnection.return_value.channel.return_value

    produce_message('sample_data.csv')

    mock_pika.BlockingConnection.assert_called_once()
    mock_channel.exchange_declare.assert_called_once_with(exchange='edits', exchange_type='direct')
    mock_channel.basic_publish.assert_called()  # Check if basic_publish was called


def test_produce_message_with_connection_error(mock_pika):
    mock_pika.BlockingConnection.side_effect = pika.exceptions.AMQPConnectionError("Connection error")

    with pytest.raises(RuntimeError, match="Error connecting to RabbitMQ:"):
        produce_message('sample_data.csv')

# Additional test cases for edge cases and error handling can be added
