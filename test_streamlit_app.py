import pytest
from streamlit_app import (
    remove_parentheses_around_numbers,
    remove_comment_tags,
    bold_complex_labels,
    format_verse_line,
    should_remove_line,
    remove_dashes_before_chords,
    process_text_content,
)

def test_remove_parentheses_around_numbers():
    assert remove_parentheses_around_numbers("[Chorus](1)") == "[Chorus]"

def test_remove_comment_tags():
    assert remove_comment_tags("{comment: Verse 1}") == "Verse 1:"

def test_bold_complex_labels_specific_patterns():
    assert bold_complex_labels("Chorus / Bridge:") == "<b>Chorus / Bridge:</b>"
    assert bold_complex_labels("Tag 1a (2X):") == "<b>Tag 1a (2X):</b>"
    assert bold_complex_labels("Bridge (2X):") == "<b>Bridge (2X):</b>"
    assert bold_complex_labels("Chorus 2a (2X):") == "<b>Chorus 2a (2X):</b>"
    assert bold_complex_labels("Chorus 2b (2X):") == "<b>Chorus 2b (2X):</b>"
    assert bold_complex_labels("Intro / Turnaround:") == "<b>Intro / Turnaround:</b>"
    # Test a label that should not be bolded
    assert bold_complex_labels("Verse 1:") == "Verse 1:"

def test_format_verse_line():
    assert format_verse_line("VERSE 1:") == "Verse 1:"
    assert format_verse_line("CHORUS 2:") == "Chorus 2:"

def test_should_remove_line():
    assert should_remove_line("{title: Amazing Grace}") is True
    assert should_remove_line("Amazing Grace") is False

def test_remove_dashes_before_chords():
    assert remove_dashes_before_chords("A - [C]mazing Grace") == "A[C]mazing Grace"

def test_process_text_content():
    input_text = """{title: Amazing Grace}
{comment: Verse 1}
A - [C]mazing grace! How sweet the sound
That saved a wretch like me."""
    expected_output = """Verse 1:
A[C]mazing grace! How sweet the sound
That saved a wretch like me."""
    assert process_text_content(input_text) == expected_output
