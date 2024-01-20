
import pytest
import display,my_connector
from wizard import Wizard
from phase import Phase
@pytest.fixture
def wizard_instance():
    return Wizard(my_connector,display)

@pytest.fixture
def mock_input(monkeypatch):
    user_inputs = []

    def mock_input_func(_=None):
        return user_inputs.pop(0)

    monkeypatch.setattr('builtins.input', mock_input_func)
    return user_inputs


def test_create_phase(wizard_instance, mock_input, capsys):
    mock_input.extend(["hamad abo", "hamad@gmail.com","28/8/98","N"])
    wizard_instance.create_phase(1)
    captured_output = capsys.readouterr()
    assert "You are in Phase 1" in captured_output.out

def test_create_phase(wizard_instance, mock_input, capsys):
    mock_input.extend(["City", "Street", "42","N"])
    wizard_instance.create_phase(2)
    captured_output = capsys.readouterr()
    assert "You are in Phase 2" in captured_output.out


def test_prev_or_next(wizard_instance, mock_input, capsys):
    mock_input.extend(["1","City", "Street", "42","3","3"])
    result = wizard_instance.prev_or_next(1)
    assert result == 'done'

def test_handle_next_move(wizard_instance,mock_input):
    mock_input.extend([ "City", "Street", "42","N"])
    result = wizard_instance.handle_next_move(1)
    assert result == 2

def test_handle_prev_move(wizard_instance,mock_input, capsys):
    wizard_instance.phases = [Phase(1)]
    mock_input.extend(["N"])
    wizard_instance.handle_prev_move(2)
    captured_output = capsys.readouterr()
    assert "Phase 1 items:" in captured_output.out


def test_start_new_wizard(wizard_instance, mock_input, capsys):
    mock_input.extend(["hamad abo","hamad1997m@gmail.com","28/8/98", "N","3","2"])

    wizard_instance.start_new_wizard()

    captured_output = capsys.readouterr()
    assert "You are in Phase 1" in captured_output.out




def test_start_wizard(wizard_instance, mock_input, capsys):
    mock_input.extend(["5"])

    wizard_instance.start_wizard()

    captured_output = capsys.readouterr()
    assert "you are out" in captured_output.out


def test_continue_wizard(wizard_instance, mock_input, capsys):
    mock_input.extend(["0","hamad","0","5"])

    wizard_instance.continue_wizard()

    captured_output = capsys.readouterr()
    assert "No wizard found with the name: hamad. Try again."  in captured_output.out
