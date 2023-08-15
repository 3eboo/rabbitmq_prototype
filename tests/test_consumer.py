from unittest.mock import Mock, patch

from consumer.consumer import EditCounter, callback


def test_edit_counter():
    counter = EditCounter()

    assert counter.global_edits == 0
    assert counter.start_time is not None

    counter.process_message('{"type": "edit"}')
    assert counter.global_edits == 1


def test_callback():
    mock_ch = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_body = b'{"type": "edit"}'
    counter = EditCounter()

    with patch('consumer.edit_counter', counter):
        callback(mock_ch, mock_method, mock_properties, mock_body)

    assert counter.global_edits == 1
