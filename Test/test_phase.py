
import pytest
from phase import Phase
from wizard import Wizard
import display,my_connector

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


def test_input_validation_valid(mock_input):
    phase =Phase(1)
    mock_input.extend(['hamd abo', 'hamad1998m@gmail.com', '01/02/100'])

    result = phase.input_validation('Enter your full name:\n', phase.validation_functions["Name"])
    assert result == 'hamd abo'


def test_input_validation_invalid_then_valid(mock_input):
    phase = Phase(1)
    mock_input.extend(['hamad', 'hamad abo'])

    result = phase.input_validation('Enter your full name:\n', phase.validation_functions["Name"])
    assert result == 'hamad abo'


def test_run_phase_phase_1_valid_inputs(mock_input,wizard_instance):
    phase = Phase(1)

    mock_input.extend(['hamad abo', 'hamad1998@gmail.com', '01/2/112'])
    phase.run_phase(wizard_instance)

    assert wizard_instance.details["Name"] == 'hamad abo'
    assert wizard_instance.details["Email"] == 'hamad1998@gmail.com'
    assert wizard_instance.details["Birth Date"] == '01/2/112'



def test_run_phase_phase_2_valid_inputs(mock_input,wizard_instance):
    phase = Phase(2)

    mock_input.extend(['hura', '22', '1'])
    phase.run_phase(wizard_instance)

    assert wizard_instance.details["City"] == 'hura'
    assert wizard_instance.details["Street"] == '22'
    assert wizard_instance.details["Number"] == '1'