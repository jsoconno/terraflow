import pytest
from terraflow.libraries.core_v2 import format_list

def test_format_list():
    # Test with no title or top
    items = ['item1', 'item2', 'item3']
    expected_output = "\n - item1\n - item2\n - item3\n"
    assert format_list(items) == expected_output

    # Test with title
    title = 'Test Title'
    expected_output = "\nTest Title\n\n - item1\n - item2\n - item3\n"
    assert format_list(items, title=title) == expected_output

    # Test with top
    top = 2
    expected_output = "\n - item1\n - item2\n"
    assert format_list(items, top=top) == expected_output

    # Test with prefix
    prefix = '* '
    expected_output = "\n* item1\n* item2\n* item3\n"
    assert format_list(items, prefix=prefix) == expected_output