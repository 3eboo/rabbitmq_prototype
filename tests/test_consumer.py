import pytest
from unittest.mock import Mock, patch
from rabbitmq_prototype.consumer.consumer import EditCounter, callback, calculate_target_per_minute

# Mocked edit_counter
edit_counter = EditCounter()

@pytest.fixture
def mock_time(monkeypatch):
    class MockTime:
        def __init__(self):
            self.start_time = 1628832000  # Mock start time to a fixed value (2021-08-14 00:00:00 UTC)

        def time(self):
            return self.start_time + 60 * edit_counter.elapsed_time_in_min

    mock_time = MockTime()
    monkeypatch.setattr('consumer.time', mock_time)
    return mock_time

def test_process_message_global_edit(mock_time):
    body = b'{"type": "edit", "server_name": "en.wikipedia.org"}'
    edit_counter.process_message(body)
    assert edit_counter.global_edits == 1
    assert edit_counter.german_wiki_edits == 0

def test_process_message_german_edit(mock_time):
    body = b'{"type": "edit", "server_name": "de.wikipedia.org"}'
    edit_counter.process_message(body)
    assert edit_counter.global_edits == 2
    assert edit_counter.german_wiki_edits == 1

def test_calculate_target_per_minute():
    target = 100
    elapsed_time = 5.0
    result = calculate_target_per_minute(target, elapsed_time)
    assert result == 20.0

def test_callback_global_edit(mock_time):
    mock_ch = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_body = b'{"type": "edit", "server_name": "en.wikipedia.org"}'

    with patch('consumer.edit_counter', edit_counter):
        callback(mock_ch, mock_method, mock_properties, mock_body)

    assert edit_counter.global_edits == 3
    assert edit_counter.german_wiki_edits == 1

def test_callback_german_edit(mock_time):
    mock_ch = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_body = b'{"type": "edit", "server_name": "de.wikipedia.org"}'

    with patch('consumer.edit_counter', edit_counter):
        callback(mock_ch, mock_method, mock_properties, mock_body)

    assert edit_counter.global_edits == 4
    assert edit_counter.german_wiki_edits == 2

def test_callback_end_message(mock_time):
    mock_ch = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_body = b'END'

    with patch('consumer.edit_counter', edit_counter):
        with patch('consumer.edit_counter.save_data') as mock_save_data:
            callback(mock_ch, mock_method, mock_properties, mock_body)

    mock_save_data.assert_called_once()

# Additional test cases for edge cases and error handling can be added
