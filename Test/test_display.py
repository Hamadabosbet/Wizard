import pytest
from display import display_summary,get_rest,show_phase
from unittest.mock import patch
details= {
            "Name": "hamad",
            "Email": "Hamad1997m@gmaol.com",
            "Birth Date": None,
            "City": None,
            "Street": None,
            "Number": None,
            "Social Media": None,
            "Hobbies": None,
            "Happy": None,
            "Skydiving": None,
            "One Dollar": None
        }
@pytest.fixture
def mock_input(monkeypatch):
    user_inputs = []

    def mock_input_func(_=None):
        return user_inputs.pop(0)

    monkeypatch.setattr('builtins.input', mock_input_func)
    return user_inputs


def test_display_summary_rest_true(mock_input):
    mock_input.extend(["1"])
    display_summary(details)
    assert get_rest() is True


def test_display_summary_rest_false(mock_input):
    mock_input.extend(["2"])
    display_summary(details)
    assert get_rest() is False


def test_show_phase_invalid(mock_input, capsys):
    with patch('builtins.print') as mock_print:
        show_phase(6, details)
        mock_print.assert_called_once_with("Invalid phase number")


def test_show_phase_valid(mock_input, capsys):
    valid_phase_number = 3
    with patch('builtins.print'):
        show_phase(valid_phase_number, details)

        captured_output = capsys.readouterr()
        assert "Invalid phase number" not in captured_output.out