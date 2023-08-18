from consumer import EditCounter


def test_edit_counter():
    counter = EditCounter()

    assert counter.global_edits == 0
    assert counter.start_time is not None

    counter.process_message(b'{"type": "edit", "server_name": "de.wikipedia.org"}')
    assert counter.global_edits == 1
    assert counter.german_wiki_edits == 1
